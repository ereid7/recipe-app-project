import React from 'react';
import { Form } from 'react-bootstrap';

const MultiSelect = ({ options, selectedOptions, onChange }) => {
  return (
    <Form.Select multiple value={selectedOptions} onChange={onChange}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </Form.Select>
  );
};

export default MultiSelect;
