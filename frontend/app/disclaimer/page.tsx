import React from 'react';

export default function DisclaimerPage() {
  return (
    <main className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-xl shadow-lg border border-slate-200">
        <h1 className="text-3xl font-bold text-black mb-8">Guarantee & Financial Projections Disclaimer</h1>
        
        <p className="mb-6 text-black leading-relaxed">
          The Data & AI Clarity Agency (operating as Fleet Clarity) provides a specialized Fleet Data Audit service. All information provided in the Instant Risk Check tool, the Video Sales Letter (VSL), and the PDF Risk Snapshot is based on publicly available FMCSA data and statistical industry models. These materials are intended for informational and compliance assessment purposes only and do not constitute financial, legal, or accounting advice.
        </p>

        <h2 className="text-xl font-bold text-black mt-8 mb-4">Performance Guarantee Limitations</h2>
        <p className="mb-6 text-black leading-relaxed">
          The $20,000 Savings Guarantee referenced in our marketing materials is a performance-based warranty that is strictly subject to the terms outlined in the final Master Service Agreement (MSA) signed upon engagement. This guarantee is exclusively available to carriers that meet the following mandatory minimum criteria at the time of the audit:
        </p>

        <ul className="list-disc pl-6 mb-6 space-y-2 text-black">
          <li>
            <strong>Fleet Size:</strong> A minimum of 20 active Power Units (trucks) listed on the carrier&apos;s MCS-150 form.
          </li>
          <li>
            <strong>Data Availability:</strong> The provision of 12 months of verifiable historical data (including raw telematics/ELD logs and fuel card transaction reports) to conduct the forensic analysis.
          </li>
        </ul>

        <h2 className="text-xl font-bold text-black mt-8 mb-4">Voiding Conditions & Liability Cap</h2>
        <p className="mb-6 text-black leading-relaxed">
          If these minimum conditions are not met, or if the client fails to provide access to the required data streams, the $20,000 guarantee is void. In the event that a qualified audit fails to identify the promised potential savings, the Company&apos;s sole liability is strictly limited to a full refund of the one-time $2,500 Audit fee.
        </p>

        <p className="mt-8 pt-8 border-t border-slate-200 text-sm text-slate-600">
          By proceeding with the service, you acknowledge that our findings are a statistical analysis of financial risk based on the data provided, and you assume all liability for any operational decisions made based on our report.
        </p>
      </div>
    </main>
  );
}
