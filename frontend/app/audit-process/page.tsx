import React from 'react';
import { ShieldCheck, Database, MapPin, FileText } from 'lucide-react';

export default function AuditProcessPage() {
  const steps = [
    {
      title: "Secure Connection",
      description: "We connect to your ELD (Motive/Samsara) and Fuel Cards (WEX/Comdata) via Read-Only APIs. No hardware installation required.",
      icon: <ShieldCheck className="h-8 w-8 text-blue-600" />
    },
    {
      title: "Forensic Ingestion",
      description: "Our engine ingests 12 months of historical data, normalizing thousands of GPS pings and transaction logs.",
      icon: <Database className="h-8 w-8 text-purple-600" />
    },
    {
      title: "The Cross-Reference",
      description: "We run proprietary algorithms to match Fuel Location vs. Truck Location and flag 'Ghost Downtime' patterns.",
      icon: <MapPin className="h-8 w-8 text-orange-600" />
    },
    {
      title: "The Findings",
      description: "You receive the Profit Protection Report, detailing exactly how much money you are losing and where.",
      icon: <FileText className="h-8 w-8 text-green-600" />
    }
  ];

  return (
    <main className="min-h-screen bg-slate-50 py-20 px-4">
      <div className="container mx-auto max-w-5xl">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">The Audit Process</h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            How we identify hidden profit leaks without disrupting your operations.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="bg-white p-8 rounded-xl shadow-lg border border-slate-100 flex gap-6 items-start hover:shadow-xl transition-shadow">
              <div className="flex-shrink-0 bg-slate-50 p-4 rounded-lg border border-slate-200">
                {step.icon}
              </div>
              <div>
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
                  Step {index + 1}
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{step.title}</h3>
                <p className="text-slate-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
