# Soli for Sublime Text

These color schemes style editor backgrounds, selections, gutters, and syntax.
They do not include a custom sidebar or tab UI theme. Sublime separates
[color schemes](https://www.sublimetext.com/docs/color_schemes.html) from
[UI themes](https://www.sublimetext.com/docs/themes.html).

## Install

1. In Sublime Text, choose **Preferences → Browse Packages**.
2. Create a `Soli` folder in the directory that opens.
3. Copy the files from `ports/sublime/schemes/` into that folder.
4. Choose **Preferences → Select Color Scheme**, then select a `Soli` scheme.

For example, your user preferences can select:

```json
{
    "color_scheme": "Soli Manna.sublime-color-scheme"
}
```

No generator or Python installation is needed. To update, replace the copied
scheme files with the latest generated versions. Package Control distribution
is not configured.

## Visual verification

Open `previews/sample.py` and inspect comments, keywords, strings, numbers,
functions, and types in each scheme. Select text and check readability; move the
caret and check its visibility. Enable line highlighting and inspect the gutter.
Use representative files in other languages to check their scope mappings.
Syntax definitions can assign different scopes, so some tokens may inherit the
ordinary foreground. Compare day and night schemes in your usual display setup.

Automated checks measure source colors, not actual application rendering or
screen-reader behavior. No browser accessibility scan applies to this port.
