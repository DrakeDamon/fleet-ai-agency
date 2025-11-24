import React from 'react';

export default function FAQPage() {
  const faqs = [
    {
      question: "Is my data safe?",
      answer: "Yes. We use Read-Only API tokens. We cannot change your data, only view it. All data is encrypted."
    },
    {
      question: "Do I qualify for the Guarantee?",
      answer: "The $20,000 Guarantee applies to fleets with 20+ active trucks and 12 months of data. Smaller fleets still benefit from the audit but do not qualify for the cash-back guarantee."
    },
    {
      question: "How long does it take?",
      answer: "The automated scan takes 3 to 5 Business Days. Your Priority Review Call happens as soon as you book it."
    }
  ];

  return (
    <main className="min-h-screen bg-slate-50 py-20 px-4">
      <div className="container mx-auto max-w-3xl">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">Frequently Asked Questions</h1>
          <p className="text-xl text-slate-600">
            Common questions about the Fleet Data Audit.
          </p>
        </div>

        <div className="space-y-6">
          {faqs.map((faq, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden">
              <div className="p-6">
                <h3 className="text-lg font-bold text-slate-900 mb-3 flex items-center gap-3">
                  <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">Q</span>
                  {faq.question}
                </h3>
                <p className="text-slate-600 pl-9 leading-relaxed">
                  {faq.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
