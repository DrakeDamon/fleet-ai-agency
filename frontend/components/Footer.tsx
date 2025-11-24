import React from 'react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 py-12 text-center text-sm">
      <div className="container mx-auto px-4">
        <p className="mb-4">The Data & AI Clarity Agency™</p>
        <p className="opacity-50 mb-4">We use public FMCSA data for qualification. Not affiliated with the DOT.</p>
        
        <div className="flex justify-center gap-4 mt-4">
            <Link href="/disclaimer" className="text-slate-500 hover:text-slate-300 transition-colors">
                Disclaimer
            </Link>
            <a href="#" className="termly-display-preferences text-slate-500 hover:text-slate-300 transition-colors">
                Consent Preferences
            </a>
        </div>
      </div>
    </footer>
  );
}
