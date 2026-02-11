/**
 * Centralized Companion Form Store
 * 
 * Single source of truth untuk character creation wizard.
 * Semua sections update store ini, submit tinggal kirim.
 */

import { writable, derived } from 'svelte/store';

export interface CompanionFormData {
  // Basic Identity
  basic: {
    name: string;
    avatar: string;
    description: string;
    category: string;
  };
  
  // Personality & Background
  personality: {
    traits: string;
    background: string;
  };
  
  // Communication Settings
  communication: {
    language: string;
    styles: string[]; // Changed from style to styles (multi-select max 3)
  };
  
  // Relationship Dynamics (7 layers)
  relationship: {
    type: string;
    role: string;
    label: string;
    customType?: string;
    customRole?: string;
    userName: string;
    preferredAddress: string;
    ageRelation: string;
    authorityLevel: string;
    emotionalTone: string;
  };
}

// Initial state
const initialFormData: CompanionFormData = {
  basic: {
    name: '',
    avatar: '🤖',
    description: '',
    category: 'supportive'
  },
  personality: {
    traits: '',
    background: ''
  },
  communication: {
    language: 'id',
    styles: ['friendly'] // Default with one style
  },
  relationship: {
    type: 'friend',
    role: 'equal',
    label: '',
    userName: '',
    preferredAddress: 'kamu',
    ageRelation: 'same',
    authorityLevel: 'equal',
    emotionalTone: 'warm'
  }
};

// Main store
export const companionForm = writable<CompanionFormData>(initialFormData);

// Current step (0-indexed)
export const currentStep = writable<number>(0);

// Validation per step
export const stepValidation = derived(companionForm, $form => ({
  0: $form.basic.name.trim() !== '' && 
     $form.basic.description.trim() !== '',
  
  1: $form.personality.traits.trim() !== '',
  
  2: $form.communication.styles.length > 0, // At least 1 style selected
  
  3: $form.relationship.userName.trim() !== '' &&
     ($form.relationship.type !== 'custom' || $form.relationship.customType?.trim() !== '') &&
     ($form.relationship.role !== 'custom' || $form.relationship.customRole?.trim() !== '')
}));

// Overall form validity
export const isFormValid = derived(stepValidation, $validation => 
  Object.values($validation).every(Boolean)
);

// Helper functions
export function updateBasic(updates: Partial<CompanionFormData['basic']>) {
  companionForm.update(form => ({
    ...form,
    basic: { ...form.basic, ...updates }
  }));
}

export function updatePersonality(updates: Partial<CompanionFormData['personality']>) {
  companionForm.update(form => ({
    ...form,
    personality: { ...form.personality, ...updates }
  }));
}

export function updateCommunication(updates: Partial<CompanionFormData['communication']>) {
  companionForm.update(form => ({
    ...form,
    communication: { ...form.communication, ...updates }
  }));
}

export function updateRelationship(updates: Partial<CompanionFormData['relationship']>) {
  companionForm.update(form => ({
    ...form,
    relationship: { ...form.relationship, ...updates }
  }));
}

export function resetForm() {
  companionForm.set(initialFormData);
  currentStep.set(0);
}

export function nextStep() {
  currentStep.update(n => Math.min(n + 1, 3));
}

export function prevStep() {
  currentStep.update(n => Math.max(n - 1, 0));
}

export function goToStep(step: number) {
  currentStep.set(Math.max(0, Math.min(step, 3)));
}

// Convert store data to API payload
export function toAPIPayload(formData: CompanionFormData) {
  return {
    name: formData.basic.name,
    avatar: formData.basic.avatar,
    description: formData.basic.description,
    category: formData.basic.category,
    personality: formData.personality.traits,
    background: formData.personality.background,
    language: formData.communication.language,
    conversationStyle: formData.communication.styles.join(', '), // Join multiple styles
    relationshipType: formData.relationship.type === 'custom' 
      ? formData.relationship.customType! 
      : formData.relationship.type,
    relationshipRole: formData.relationship.role === 'custom'
      ? formData.relationship.customRole!
      : formData.relationship.role,
    relationshipLabel: formData.relationship.label,
    userName: formData.relationship.userName || formData.basic.name,
    preferredAddress: formData.relationship.preferredAddress,
    ageRelation: formData.relationship.ageRelation,
    authorityLevel: formData.relationship.authorityLevel,
    emotionalTone: formData.relationship.emotionalTone
  };
}
