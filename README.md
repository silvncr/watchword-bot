<!-- omit in toc -->
# Watchword Dictionary

<!-- omit in toc -->
## Contents

- [Usage](#usage)
- [Structure](#structure)
  - [Wordlist data](#wordlist-data)
  - [Wordlist types](#wordlist-types)
    - [Word flags](#word-flags)
  - [Watchword versions](#watchword-versions)
    - [Adding support for a new version](#adding-support-for-a-new-version)
  - [Other data](#other-data)
    - [Word definitions](#word-definitions)
- [Changelog](#changelog)
  - [Discord bot](#discord-bot)

## Usage

This repository contains the data files for the Watchword game dictionary, which are used by the following tools:

- There is an interactive web interface available here: <https://silvncr.github.io/watchword-dictionary/>
- There is also a Discord bot, but its uptime is not guaranteed. You can add it to your profile or server here: <https://discord.com/oauth2/authorize?client_id=1376949038061981860>

## Structure

### Wordlist data

Wordlists are stored in the `/data/` directory. Filenames follow the format of `<version>_<type>.txt`, where:

- `<version>` is the game version number: `X.Y.Z`.
- `<type>` is the type of wordlist; [explained below](#wordlist-types)

For example, `1.0.0_wordlist.txt` or `1.0.0_badlist.txt`.

The wordlist contents are formatted according to [`silvncr/wordlist-cleaner#wordlist-format`](https://github.com/silvncr/wordlist-cleaner#wordlist-format), which is a simple text format with one word per line.

> [!NOTE]
> Wordlists are sourced from the game files, however they may have their formatting modified, like a text case transformation. The term "riplist" is used to refer to files which have NOT been modified in this way. This term isn't used in the filenames, but it might still appear in the code.

### Wordlist types

`/data/watchword_flags.json` contains a dictionary that describes the flags imbued by each wordlist type. Keys are types, values are a list of flags.

#### Word flags

Flags are applied to words to give them different behaviours in-game.

> [!IMPORTANT]
> All flag names are subject to change. Please view the file to see the latest relationships.
>
> This system is intended to reflect the game's behaviour, but it's ultimately arbitrary. There may be discrepancies. Where possible, it will be updated to better reflect what happens in-game.

### Watchword versions

- `/data/watchword_versions.json` contains a list of supported Watchword versions. The newest version is always at the top of the list.
- `/data/watchword_references.json` holds the data for changes in the wordlist between versions. Version names are used as keys, and the values are links to the oldest version that has the same wordlist. Values of `null` indicate changes in the wordlist.

> [!TIP]
> Having newer versions higher on the list keeps git diffs cleaner.

#### Adding support for a new version

To add support for a new Watchword version, you must do all of the following:

- Verify the wordlist for the new version by ripping it from the game files.

  - You need to decompile the game files. A guide may be created in the future.
  - If the version is old, you'll have to download the old version with an external tool.

- Use an external tool to check whether the wordlist has changed since the last version.

  If the list has changed, add the new wordlist(s) to `/data/` in the format described [above](#wordlist-data).

- Add the version name to `/data/watchword_references.json`. New versions should be added at the top of the list.

  - If the wordlists are identical to an existing version, use the name of that version as the value.
  - If the wordlist was changed in the current update, set the value to `null`.

- Add the version name to `/data/watchword_versions.json`. New versions should be added at the top of the list.

### Other data

#### Word definitions

- `/data/dictionary_combined.json` stores the definitions of known words, and is compiled from various online sources. Note that not all words in the Watchword dictionary are defined. You can check the dictionary coverage for a wordlist version with the `/info coverage` command, ~~or interactively in the web interface~~ (coming soon).

## Changelog

### Discord bot

0.3.x

- Added flags system
  - Multiple wordlists are compiled on load to closer reflect in-game behaviour
  - Flag names are arbitrary; it's up to the user to discern what they mean

0.2.x

- Added dictionary functionality
  - Definitions appear under `/check` result
  - Added `/coverage` command to see an overview of dictionary data
- Added support for multiple game versions
  - `/check` and `/coverage` now have a `version:` parameter
  - The newest version is selected by default

0.1.x

- Added basic `/check` command; check if a word is valid or invalid
