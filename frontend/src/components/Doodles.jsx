import React from 'react';

export function Sparkle({ className = "" }) {
  return (
    <svg className={`overflow-visible ${className}`} width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 2 Q 16 14 28 16 Q 16 18 16 30 Q 16 18 4 16 Q 16 14 16 2 Z" fill="currentColor" opacity="0.9"/>
    </svg>
  );
}

export function SquiggleUnderline({ className = "" }) {
  return (
    <svg className={`overflow-visible ${className}`} width="100%" height="16" viewBox="0 0 120 16" preserveAspectRatio="none" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round">
      <path d="M 3 10 Q 15 2 30 8 T 60 7 T 90 9 T 117 5" />
    </svg>
  );
}

export function CurvedArrow({ className = "" }) {
  return (
    <svg className={`overflow-visible ${className}`} width="60" height="60" viewBox="0 0 60 60" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <path d="M 10 50 C 20 20, 40 10, 50 30" />
      <path d="M 50 30 L 38 25" />
      <path d="M 50 30 L 45 42" />
    </svg>
  );
}

export function ScribbleMark({ className = "" }) {
  return (
    <svg className={`overflow-visible ${className}`} width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M 5 15 C 25 5, 10 35, 35 25" />
      <path d="M 15 5 C 35 20, 5 30, 25 35" />
    </svg>
  );
}
