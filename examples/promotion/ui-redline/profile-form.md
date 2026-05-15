# Component Spec: ProfileSettingsForm

## Anatomy
- `FormContainer`
  - `FieldGroup`
    - `Label` (Display Name)
    - `TextInput`
  - `FieldGroup`
    - `Label` (Profile Picture)
    - `AvatarUpload`
      - `ImagePreview`
      - `UploadButton`
      - `HelperText`

## State Matrix
| Element | Default | Focus | Error | Disabled |
|---------|---------|-------|-------|----------|
| `TextInput` | `border-default` | `ring-2 ring-action-primary` | `border-red-500` | `bg-gray-100 cursor-not-allowed` |
| `UploadButton`| `text-action-primary` | `underline` | - | `text-disabled` |

## Accessibility
- Use `<form>` tag.
- Upload button must be keyboard accessible (triggerable via Enter/Space).
- Input must use `aria-invalid` if there is an error.
