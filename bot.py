from __future__ import annotations

import json
import os
from pathlib import Path
from string import ascii_uppercase

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()


TOKEN = os.environ['DISCORD_TOKEN']

VERSION = '0.3.2'


WATCHWORD_REFERENCES: dict[str, str | None] = json.loads(
    Path('data', 'watchword_references.json').read_text(),
)
WATCHWORD_VERSIONS: list[str] = json.loads(
    Path('data', 'watchword_versions.json').read_text(),
)


def find_reference(version: str) -> str:
    '''Find the reference for a given version.'''
    if WATCHWORD_REFERENCES[version] is None:
        return version
    return find_reference(WATCHWORD_REFERENCES[version])  # type: ignore


def create_version_string(version: str) -> str:
    '''Create a game version string with reference.'''
    version_referenced = find_reference(version)
    if version == version_referenced:
        return version
    return f'{version_referenced} -> {version}'


OPTIONS = {
    'version': nextcord.SlashOption(
        name='version',
        description='The Watchword game version to check against',
        required=False,
        choices=[*WATCHWORD_VERSIONS],
        default=WATCHWORD_VERSIONS[0],
        verify=True,
    ),
    'word': nextcord.SlashOption(
        name='word',
        description='The word to check against the Watchword dictionary',
        required=True,
        min_length=2,
        max_length=40,
        verify=True,
    ),
}


client = commands.Bot(
    description=f'Watchword Dictionary v{VERSION}', intents=nextcord.Intents.default(),
)


def embed(title: str, description: str, color: int = 0xFFFFFF) -> nextcord.Embed:
    '''Create a simple embed.'''
    return (
        nextcord.Embed(title=title, description=description, color=color)
        # .set_author(
        #     name='Watchword Dictionary',
        #     icon_url='https://cdn.discordapp.com/icons/1327739235121496125/6273973dd811f41333d22f2dc2a1baeb.webp',
        # )
        .set_footer(text=f'v{VERSION}')
    )


def find_definition(word: str) -> str | None:
    '''Find the definition of a word in the wordlist.'''
    return definitions.get(word)


@client.event
async def on_ready() -> None:
    '''Event triggered when the bot is ready.'''
    print(f'Logged in as {client.user} (ID: {client.user.id})')  # type: ignore
    await client.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching,
            name=f'for {len(wordlist_full):,} words',
        ),
        status=nextcord.Status.online,
    )


@client.slash_command(
    name='check', description='Check against the Watchword dictionary',
)
async def check(
    interaction: nextcord.Interaction,
    word: str = OPTIONS['word'],
    version: str = OPTIONS['version'],
) -> None:
    '''Check a word against the Watchword dictionary.'''
    print(f'Word check by {interaction.user} ({interaction.user.id}) - "{word}"')  # type: ignore
    word = word.upper().strip()
    word = ''.join(c for c in word if c in ascii_uppercase)
    print(f'\tProcessed: "{word}"')
    for x, y in [
        (any(c not in ascii_uppercase for c in word), 'Words must have letters only!'),
        (not 2 <= len(word) <= 40, 'Words must be between 2 and 40 characters long!'),
    ]:
        if x:
            await interaction.response.defer(ephemeral=True)
            print(f'\tInvalid input: "{y}"')
            await interaction.followup.send(
                f':warning: Invalid input: `{word or '(empty)'}`\n> {y}',
            )
            return
    await interaction.response.defer()
    version_referenced = find_reference(version)
    version_string = create_version_string(version)
    if word in wordlists[version_referenced]:
        print('\tValid word')
        _embed = embed(
            title=f':white_check_mark: {word}',
            description=f'This is a valid word in Watchword {version_string}',
            color=0x00FF00,
        )
        if _definition := find_definition(word):
            print(f'\tDefinition found: "{_definition}"')
            _embed=_embed.add_field(
                name='Definition', value=f'```\n{_definition}\n```', inline=False,
            )
        else:
            print('\tNo definition found')
        print(f'\tFlags: {(_flags := wordlists[version_referenced][word])}')
        _embed.add_field(
            name='Flags',
            value=f'{', '.join(_flags)}' if _flags else '(none)',
            inline=False,
        )
        await interaction.followup.send(embed=_embed)
    else:
        print('\tInvalid word')
        await interaction.followup.send(
            embed=embed(
                title=f':x: {word}',
                description=(f'This is not a valid word in Watchword {version_string}'),
                color=0xFF0000,
            ),
        )


@client.slash_command(
    name='info', description='Get information about the Watchword Dictionary bot',
)
async def info(interaction: nextcord.Interaction) -> None:
    '''Parent command.'''


@info.subcommand(name='coverage', description='Get the coverage of word definitions')
async def coverage(
    interaction: nextcord.Interaction, version: str = OPTIONS['version'],
) -> None:
    '''Get the coverage of word definitions in the Watchword dictionary.'''
    await interaction.response.defer(ephemeral=True)
    version_ref = find_reference(version)
    version_s = create_version_string(version)
    _words = len(wordlists[version_ref])
    _definitions = len({word for word in definitions if word in wordlists[version_ref]})
    await interaction.followup.send(
        embed=embed(
            title=':bar_chart: Coverage',
            description=f'**{version_s}**```\n{
                '\n'.join(
                    [
                        f'words: {_words:,}',
                        f'definitions: {_definitions:,}',
                        f'coverage: {_definitions / _words * 100:.2f}%',
                    ]
                )
            }\n```',
        ),
    )
    print(f'Coverage requested by {interaction.user} ({interaction.user.id})')  # type: ignore


@info.subcommand(name='ping', description='Returns bot latency')
async def ping(interaction: nextcord.Interaction) -> None:
    '''Ping command to check bot latency.'''
    await interaction.response.defer(ephemeral=True)
    _latency: float = round(client.latency * 100, 2)
    await interaction.followup.send(
        embed=embed(title=':ping_pong: Pong!', description=f'```\n{_latency} ms\n```'),
    )
    print(f'Ping by {interaction.user} ({interaction.user.id}) - {_latency} ms')  # type: ignore


if __name__ == '__main__':
    wordlists: dict[str, dict[str, set]] = {}
    wordlist_full: set[str] = set()
    for _version in WATCHWORD_VERSIONS:
        if _version != find_reference(_version):
            continue
        print(f'Loading wordlist for version {_version}..')
        wordlists[_version] = {}
        for _type, _flags in {
            'wordlist': set(),
            'badlist': {'bad'},
            'cleanlist': {'clean'},
        }.items():
            if (_path := Path('data', 'wordlists', f'{_version}_{_type}.txt')).exists():
                wordlists[_version] |= {
                    word.strip().upper():
                    wordlists[_version].get(word.strip().upper(), set()) | _flags
                    for word in _path.read_text().strip().splitlines()
                }
        if not wordlists[_version]:
            print('\tNo wordlist found, skipping..')
            continue
        print(f'\tLoaded {len(wordlists[_version]):_} words')
        wordlist_full.update(wordlists[_version].keys())

    print(f'Loaded {len(wordlist_full):_} total words')

    all_definitions = json.loads(Path('data', 'dictionary_combined.json').read_text())
    definitions = {
        key: val for key, val in all_definitions.items() if key in wordlist_full
    }
    del all_definitions
    print(f'Loaded {len(definitions):_} definitions')

    client.run(TOKEN)
