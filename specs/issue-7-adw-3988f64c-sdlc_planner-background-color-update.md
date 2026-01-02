# Chore: Background Color Update to Light Green

## Metadata
issue_number: `7`
adw_id: `3988f64c`
issue_json: `{"number":7,"title":"Background color update","body":"/chore - adw_sdlc_zte_iso - Update the background color to the equivalent light green color"}`

## Chore Description
Update the application's background color from the current light sky blue (#E0F6FF) to an equivalent light green color. This change will provide a fresh, calming appearance while maintaining excellent readability and visual hierarchy across the application. The light green color should be subtle enough to not interfere with existing UI components while providing the desired visual update.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/style.css` - Contains the CSS color variables including the `--background` variable that controls the application's background color (line 9). This is the primary file that needs to be modified.
- `app_docs/feature-f055c4f8-off-white-background.md` - Reference documentation showing the history of background color changes and the CSS variable system used.
- `app_docs/feature-6445fc8f-light-sky-blue-background.md` - Reference documentation showing the most recent background color change to light sky blue, which this chore will replace with light green.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update Background Color CSS Variable
- Open `app/client/src/style.css`
- Locate the `--background` CSS variable on line 9 (currently set to `#E0F6FF`)
- Change the value from `#E0F6FF` (light sky blue) to `#E0FBE0` (light green)
- The light green color `#E0FBE0` is chosen because:
  - It provides a similar luminosity and saturation to the current light sky blue
  - It maintains excellent readability with existing text colors
  - It's subtle enough to not interfere with existing UI components
  - It provides a fresh, calming appearance

### 2. Run Validation Commands
- Execute all validation commands listed below to ensure the chore is complete with zero regressions
- Verify that the server tests pass
- Build the client application to ensure no build errors
- Visually confirm the light green background is applied correctly

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `cd app/client && bun run build` - Build the frontend to ensure no TypeScript or build errors occur

## Notes
- The light green color `#E0FBE0` was selected to match the luminosity and saturation of the previous light sky blue `#E0F6FF`
- This change only affects the visual appearance and does not modify any functionality
- All existing UI components, text colors, and visual hierarchy will work correctly with the new background
- The CSS variable system makes this change simple - only one line needs to be modified
- No other color variables need adjustment as they are designed to work with light backgrounds
- The change will be automatically applied across the entire application once the CSS is rebuilt
