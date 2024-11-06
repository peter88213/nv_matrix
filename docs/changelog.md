[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog

### Version 4.6.2

No longer disable the "Matrix" menu entry when locking the project.

Compatible with novelibre 4.11
Based on apptk 2.2.0

### Version 4.6.1

- Fix a bug where the project lock has no effect on user operation.
- Fix a bug where the "Close" button moves to a wrong position after refreshing the view.
- Change the window title.

Refactor for better maintainability:

- Make the TableManager a ViewComponentBase subclass.
- Link the source code to the new "apptk" GUI library.
- Replae global constants with class constants.
- Move platform-specific modules to their own package.

Compatible with novelibre 4.11
Based on apptk 2.2.0

### Version 4.6.0

- Add tootlip.

Refactor:
- Separate keyboard settings and mouse operation settings.
- Put everything in the new platform_settings module.

Compatibility: novelibre 4.11 API
Based on novxlib 4.6.4

### Version 4.5.2

- Refactor the event bindings.

Compatibility: novelibre 4.5 API
Based on novxlib 4.6.4

### Version 4.5.1

- Fix a regression from version 4.5.0 where the "Quit" key does not work on non-Windows platforms.
- Refactor: Undo some renamings from version 4.5.0.
- Consider FreeBSD.

Compatibility: novelibre 4.5 API
Based on novxlib 4.6.4

### Version 4.5.0

- Provide shortcuts and key bindings for Mac OS.
- Refactor event bindings.
- Automatically resize the setup window.

Compatibility: novelibre 4.5 API
Based on novxlib 4.6.4

### Version 4.4.2

- Refactor: Change import order for a quick start.

Compatibility: novelibre 4.5 API
Based on novxlib 4.6.3

### Version 4.4.1

- Fix localization issues by updating to novxlib v4.4.2.

### Version 4.4.0

- Fix a bug where the novelibre desktop mouse scrolling takes effect on the matrix view.
- novelibre API update.

Compatibility: novelibre 4.5 API
Based on novxlib 4.4.0

### Version 4.3.2

- Refactor localization.

Compatibility: novelibre 4.3 API
Based on novxlib 4.4.0

### Version 4.3.1

- Handle minimized window.

Compatibility: novelibre 4.3 API
Based on novxlib 4.4.0

### Version 4.3.0

- Move the **Matrix** entry from the main menu to the **Tools** menu.
- Add a "Matrix" button to the button bar.

Compatibility: novelibre 4.3 API
Based on novxlib 4.4.0

### Version 4.2.2

- Library update.

Compatibility: novelibre 4.3 API
Based on novxlib 4.3.0

### Version 4.2.1

- Refactor the code for future API update,
  making the prefs argument of the Plugin.install() method optional.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.2.0

- Refactor the code for better maintainability.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.1.0

- Use a novelibre service factory method instead of importing the novxlib configuration module.

Compatibility: novelibre 4.1 API

### Version 3.0.1

- On Windows, do not assign the Ctrl Q shortcut for closing.
- Add a "Close" button.

Based on novxlib 2.0.1
Compatibility: novelibre 3.0 API

### Version 3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Based on novxlib 2.0.0
Compatibility: novelibre 3.0 API

### Version 2.2.1

- Rewording: Arc -> Plot line.

Based on novxlib 1.5.0
Compatibility: noveltree 2.1 API

### Version 2.2.0

- Implement global locking and unlocking.

Based on novxlib 1.1.0
Compatibility: noveltree 2.1 API

### Version 2.1.0

Update for "novelibre".

Based on novxlib 1.1.0
Compatibility: noveltree 2.1 API

### Version 2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Based on novxlib 1.1.0
Compatibility: noveltree 2.0 API

### Version 1.1.0

- Re-structure the website; adjust links.

Based on novxlib 1.1.0
Compatibility: noveltree 1.8 API

### Version 1.0.3

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.2

- Fix a bug where the matrix view is not refreshed on element changes made with noveltree.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.1

- Fix the plugin API version constant.
- Update the build process.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.0

- Release under the GPLv3 license.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API
