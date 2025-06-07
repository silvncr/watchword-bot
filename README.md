<!-- omit in toc -->
# Watchword Dictionary

<!-- omit in toc -->
## Contents

- [Usage](#usage)
- [Structure](#structure)
  - [Wordlist data](#wordlist-data)
  - [Watchword versions](#watchword-versions)
    - [Adding support for a new version](#adding-support-for-a-new-version)
  - [Other data](#other-data)
    - [Word definitions](#word-definitions)

## Usage

This repository contains the data files for the Watchword game dictionary, which are used by the following tools:

- There is an interactive web interface available here: <https://silvncr.github.io/watchword-dictionary/>
- There is also a Discord bot, but its uptime is not guaranteed. You can add it to your profile or server here: <https://discord.com/oauth2/authorize?client_id=1376949038061981860>

## Structure

### Wordlist data

Wordlists are stored in the `/data/` directory. Filenames follow the format of `watchword_wordlist_<version>.txt`, where `<version>` is the game version number. Demo versions are prefixed with `demo-`.

The wordlist contents are formatted according to [`silvncr/wordlist-cleaner#wordlist-format`](https://github.com/silvncr/wordlist-cleaner#wordlist-format), which is a simple text format with one word per line. **Any listed warnings from the wordlist cleaner apply to these wordlists.**

Wordlists are ripped from the game files. If you see the term "riplists" in the code, it refers to these wordlists. That is to say, a riplist is a wordlist that is sourced directly from the game files, verified by the repo contributors.

### Watchword versions

- `/data/watchword_versions.json` contains a list of supported Watchword versions. The newest version is always at the top of the list.
- `/data/watchword_references.json` holds the data for changes in the wordlist between versions. Version names are used as keys, and the values are links to the oldest version that has the same wordlist. Values of `null` indicate changes in the wordlist.

#### Adding support for a new version

To add support for a new Watchword version, you must do all of the following:

- Verify the wordlist for the new version by ripping it from the game files.

  You'll have to download the old version, and decompile the game files. A guide may be created in the future.

- Use an external tool to check whether the wordlist has changed since the last version.

  If the list has changed, add the new wordlist to `/data/` in the format described [above](#wordlist-data).

- Add the version name to `/data/watchword_references.json`. New versions should be added at the top of the list.

  - If the wordlist is identical to an existing version, use the name of that version as the value.
  - If the wordlist was changed in the current update, set the value to `null`.

- Add the version name to `/data/watchword_versions.json`. New versions should be added at the top of the list.

### Other data

#### Word definitions

- `/data/dictionary_combined.json` stores the definitions of known words, and is compiled from various online sources. Note that not all words in the Watchword dictionary are defined. You can check the dictionary coverage for a wordlist version with the `/info coverage` command, or interactively in the web interface.
