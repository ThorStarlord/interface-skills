export function ProfileSettingsForm({ error, disabled }) {
  return (
    <div className="form-container">
      <div className="field-group">
        <label>Display Name</label>
        <input
          type="text"
          className={`border ${error ? 'border-red-500' : 'border-default'} focus:outline-none`}
          disabled={disabled}
        />
      </div>
      <div className="field-group">
        <label>Profile Picture</label>
        <div className="avatar-upload">
          <div className="image-preview" />
          <span className="text-blue-500 cursor-pointer" onClick={() => {}}>Upload</span>
          <p className="helper-text">Max 2MB</p>
        </div>
      </div>
    </div>
  )
}
