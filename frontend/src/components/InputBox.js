import React from 'react';
import '../styles/InputBox.css';

function InputBox({ value, onChange, disabled, placeholder }) {
  return (
    <input
      type="text"
      className="input-box"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
      placeholder={placeholder || 'Type your question here...'}
    />
  );
}

export default InputBox;
