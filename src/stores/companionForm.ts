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
    gender: 'Male' | 'Female';
    race: string;
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
  
  // Relationship Dynamics (SIMPLIFIED)
  relationship: {
    type: string;              // friend, partner, mentor, student, rival
    label: string;             // Optional custom label
    userName: string;          // User's name
    preferredAddress: string;  // casual, respectful, intimate
  };
}

// Initial state
const initialFormData: CompanionFormData = {
  basic: {
    name: '',
    avatar: 'default-1',
    gender: 'Female',
    race: 'asian',
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
    label: '',
    userName: '',
    preferredAddress: 'casual'
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

// Helper: Convert race ID to label
const raceIdToLabel: Record<string, string> = {
  'asian': 'Asian',
  'caucasian': 'Caucasian',
  'african': 'African',
  'hispanic': 'Hispanic',
  'middle-eastern': 'Middle Eastern',
  'indigenous': 'Indigenous',
  'pacific-islander': 'Pacific Islander',
  'mixed': 'Mixed',
  'elf': 'Elf',
  'dwarf': 'Dwarf',
  'vampire': 'Vampire',
  'werewolf': 'Werewolf',
  'fairy': 'Fairy',
  'demon': 'Demon',
  'angel': 'Angel',
  'dragon': 'Dragon',
  'mermaid': 'Mermaid',
  'wizard': 'Wizard',
  'android': 'Android',
  'alien': 'Alien'
};

// Convert store data to API payload
export function toAPIPayload(formData: CompanionFormData) {
  // Map preferredAddress to backend format
  const addressMapping: Record<string, string> = {
    'casual': 'kamu',
    'respectful': 'mas',  // or 'mbak' depending on character gender
    'intimate': 'sayang'
  };

  return {
    name: formData.basic.name,
    avatar: formData.basic.avatar,
    gender: formData.basic.gender,
    race: raceIdToLabel[formData.basic.race] || formData.basic.race,
    description: formData.basic.description,
    category: formData.basic.category,
    personality: formData.personality.traits,
    background: formData.personality.background,
    language: formData.communication.language,
    conversationStyle: formData.communication.styles.join(', '),
    relationshipType: formData.relationship.type,
    relationshipRole: 'equal',  // Default to equal (simplified)
    relationshipLabel: formData.relationship.label || formData.relationship.type,
    userName: formData.relationship.userName || 'User',
    preferredAddress: addressMapping[formData.relationship.preferredAddress] || 'kamu',
    ageRelation: 'same',  // Default (simplified)
    authorityLevel: 'equal',  // Default (simplified)
    emotionalTone: 'warm'  // Default (simplified)
  };
}
