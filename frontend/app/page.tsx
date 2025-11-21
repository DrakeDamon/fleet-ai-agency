import type { Metadata } from "next";
import LeadForm from "../components/LeadForm";
import { Check, TrendingUp, AlertTriangle, ShieldAlert } from "lucide-react";

export const metadata: Metadata = {
  title: "Fleet Data Audit | Cut Downtime & Fuel Fraud",
  description: "Specialized AI diagnostics for fleets with 10-100 trucks. Uncover hidden costs in your ELD and Fuel data.",
};

export default function Home() {
  // JSON-LD for SEO
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "The Data & AI Clarity Agency",
    "description": "Data engineering and AI audits for trucking fleets.",
    "areaServed": "US",
    "priceRange": "$$$"
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Inject JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* HERO SECTION */}
      <section className="relative bg-slate-900 text-white pt-20 pb-32 overflow-hidden">
        <div className="container mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
          <div className="z-10">
            <div className="inline-block bg-blue-600/20 text-blue-300 px-3 py-1 rounded-full text-sm font-semibold mb-6 border border-blue-500/30">
              For Fleets with 10–100 Power Units
            </div>
            <h1 className="text-5xl font-bold leading-tight mb-6">
              Stop Bleeding Profit to <span className="text-blue-400">Breakdowns</span> & <span className="text-orange-400">Fraud</span>.
            </h1>
            <p className="text-xl text-slate-300 mb-8 max-w-lg">
              Most fleets are drowning in data but starving for insights. We use AI to audit your TMS & Telematics data and find your hidden cost-per-mile leaks.
            </p>
            <div className="flex flex-col gap-3 text-slate-400">
              <div className="flex items-center gap-2"><Check className="text-green-400" /> No new software to install</div>
              <div className="flex items-center gap-2"><Check className="text-green-400" /> Works with Samsara, Motive, Geotab</div>
            </div>
          </div>
          
          <div className="z-10">
            <LeadForm />
          </div>
        </div>
      </section>

      {/* TRUST BAR */}
      <div className="bg-slate-100 border-b border-slate-200 py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-slate-500 font-semibold tracking-wider uppercase mb-4">Built on Industrial Data Standards</p>
          <div className="flex justify-center gap-8 opacity-50 grayscale text-slate-700 font-bold text-xl">
            <span>Snowflake</span>
            <span>dbt</span>
            <span>Python</span>
            <span>FMCSA Data</span>
          </div>
        </div>
      </div>

      {/* PAIN POINTS */}
      <section className="py-24 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16">The &quot;Hidden Cost&quot; Triad</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Card 1 */}
            <div className="p-8 border border-slate-100 shadow-lg rounded-xl bg-white">
              <div className="bg-red-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <AlertTriangle className="text-red-600" />
              </div>
              <h3 className="text-xl font-bold mb-3">Unplanned Downtime</h3>
              <p className="text-slate-600">
                A roadside breakdown costs an average of <strong>$448/hour</strong> plus towing. Our audit predicts failure patterns before the check engine light comes on.
              </p>
            </div>
             {/* Card 2 */}
             <div className="p-8 border border-slate-100 shadow-lg rounded-xl bg-white">
              <div className="bg-orange-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <ShieldAlert className="text-orange-600" />
              </div>
              <h3 className="text-xl font-bold mb-3">Fuel Fraud & Theft</h3>
              <p className="text-slate-600">
                Are your fuel cards matching your GPS locations? We cross-reference datasets to find the <strong>$2k-$10k/month</strong> leaks you can&apos;t see manually.
              </p>
            </div>
             {/* Card 3 */}
             <div className="p-8 border border-slate-100 shadow-lg rounded-xl bg-white">
              <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
                <TrendingUp className="text-blue-600" />
              </div>
              <h3 className="text-xl font-bold mb-3">True CPM Clarity</h3>
              <p className="text-slate-600">
                Stop guessing your profitability. We merge finance and operations data to give you a precise, real-time Cost Per Mile for every lane.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-slate-900 text-slate-400 py-12 text-center text-sm">
        <div className="container mx-auto px-4">
          <p className="mb-4">The Data & AI Clarity Agency™</p>
          <p className="opacity-50">We use public FMCSA data for qualification. Not affiliated with the DOT.</p>
        </div>
      </footer>
    </main>
  );
}
