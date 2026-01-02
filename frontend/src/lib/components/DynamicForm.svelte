<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  // Types
  interface FormField {
    name: string;
    type: 'text' | 'number' | 'date' | 'select' | 'boolean';
    label: string;
    required: boolean;
    description?: string;
    default?: any;
    options?: string[];
    min?: number;
    max?: number;
  }

  interface DynamicFormSchema {
    toolName: string;
    serverName: string;
    description?: string;
    fields: FormField[];
  }

  // Props
  export let schema: DynamicFormSchema | null = null;
  export let loading = false;
  export let disabled = false;

  // State
  let formData: Record<string, any> = {};
  let errors: Record<string, string> = {};

  const dispatch = createEventDispatcher<{
    submit: Record<string, any>;
  }>();

  // Initialize form data from schema defaults
  $: if (schema) {
    formData = {};
    schema.fields.forEach(field => {
      formData[field.name] = field.default ?? (field.type === 'boolean' ? false : '');
    });
    errors = {};
  }

  function validate(): boolean {
    errors = {};
    let isValid = true;

    if (!schema) return false;

    schema.fields.forEach(field => {
      const value = formData[field.name];
      
      if (field.required && (value === '' || value === null || value === undefined)) {
        errors[field.name] = `${field.label} is required`;
        isValid = false;
      }
      
      if (field.type === 'number' && value !== '' && value !== null) {
        const num = Number(value);
        if (isNaN(num)) {
          errors[field.name] = `${field.label} must be a number`;
          isValid = false;
        } else {
          if (field.min !== undefined && num < field.min) {
            errors[field.name] = `${field.label} must be at least ${field.min}`;
            isValid = false;
          }
          if (field.max !== undefined && num > field.max) {
            errors[field.name] = `${field.label} must be at most ${field.max}`;
            isValid = false;
          }
        }
      }
    });

    return isValid;
  }

  function handleSubmit() {
    if (validate()) {
      // Clean up empty optional fields
      const cleanData: Record<string, any> = {};
      Object.entries(formData).forEach(([key, value]) => {
        if (value !== '' && value !== null && value !== undefined) {
          cleanData[key] = value;
        }
      });
      dispatch('submit', cleanData);
    }
  }
</script>

<div class="dynamic-form">
  {#if !schema}
    <div class="no-schema">
      <p>Select a tool to generate the form</p>
    </div>
  {:else}
    <div class="form-header">
      <h3>{schema.toolName.replace(/_/g, ' ').replace(/-/g, ' ')}</h3>
      {#if schema.description}
        <p class="description">{schema.description}</p>
      {/if}
    </div>

    <form on:submit|preventDefault={handleSubmit}>
      {#each schema.fields as field}
        <div class="form-field" class:has-error={errors[field.name]}>
          <label for={field.name}>
            {field.label}
            {#if field.required}
              <span class="required">*</span>
            {/if}
          </label>

          {#if field.type === 'text'}
            <input
              type="text"
              id={field.name}
              bind:value={formData[field.name]}
              placeholder={field.description || ''}
              disabled={disabled || loading}
            />
          {:else if field.type === 'number'}
            <input
              type="number"
              id={field.name}
              bind:value={formData[field.name]}
              min={field.min}
              max={field.max}
              placeholder={field.description || ''}
              disabled={disabled || loading}
            />
          {:else if field.type === 'date'}
            <input
              type="date"
              id={field.name}
              bind:value={formData[field.name]}
              disabled={disabled || loading}
            />
          {:else if field.type === 'select' && field.options}
            <select
              id={field.name}
              bind:value={formData[field.name]}
              disabled={disabled || loading}
            >
              <option value="">Select {field.label}...</option>
              {#each field.options as option}
                <option value={option}>{option}</option>
              {/each}
            </select>
          {:else if field.type === 'boolean'}
            <label class="checkbox-label">
              <input
                type="checkbox"
                id={field.name}
                bind:checked={formData[field.name]}
                disabled={disabled || loading}
              />
              <span>{field.description || 'Enable'}</span>
            </label>
          {/if}

          {#if field.description && field.type !== 'boolean'}
            <small class="hint">{field.description}</small>
          {/if}

          {#if errors[field.name]}
            <small class="error">{errors[field.name]}</small>
          {/if}
        </div>
      {/each}

      <button type="submit" class="submit-btn" disabled={disabled || loading}>
        {#if loading}
          <span class="spinner"></span>
          Executing...
        {:else}
          Execute Tool
        {/if}
      </button>
    </form>
  {/if}
</div>

<style>
  .dynamic-form {
    background: rgba(20, 20, 30, 0.8);
    border: 1px solid rgba(100, 100, 150, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
  }

  .no-schema {
    text-align: center;
    color: #888;
    padding: 2rem;
  }

  .form-header h3 {
    margin: 0 0 0.5rem 0;
    color: #fff;
    text-transform: capitalize;
    font-size: 1.25rem;
  }

  .form-header .description {
    color: #aaa;
    font-size: 0.875rem;
    margin: 0 0 1.5rem 0;
    line-height: 1.5;
  }

  .form-field {
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #ccc;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .required {
    color: #ff6b6b;
    margin-left: 2px;
  }

  input[type="text"],
  input[type="number"],
  input[type="date"],
  select {
    width: 100%;
    padding: 0.75rem 1rem;
    background: rgba(30, 30, 45, 0.9);
    border: 1px solid rgba(100, 100, 150, 0.4);
    border-radius: 8px;
    color: #fff;
    font-size: 0.95rem;
    transition: all 0.2s ease;
  }

  input:focus,
  select:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
  }

  input:disabled,
  select:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  input::placeholder {
    color: #666;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
    color: #ccc;
  }

  .checkbox-label input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #6366f1;
  }

  .hint {
    display: block;
    margin-top: 0.375rem;
    color: #777;
    font-size: 0.75rem;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .error {
    display: block;
    margin-top: 0.375rem;
    color: #ff6b6b;
    font-size: 0.75rem;
  }

  .has-error input,
  .has-error select {
    border-color: #ff6b6b;
  }

  .submit-btn {
    width: 100%;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border: none;
    border-radius: 8px;
    color: #fff;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
  }

  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
  }

  .submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
