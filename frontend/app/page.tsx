import type { Metadata } from "next";
import LeadForm from "../components/LeadForm";
import Hero from "../components/Hero";
import { Check, TrendingUp, AlertTriangle, ShieldAlert } from "lucide-react";

export const metadata: Metadata = {
  title: "Fleet Data Audit | Cut Downtime & Fuel Fraud",
  description: "Specialized AI diagnostics for fleets with 20-100 trucks. Uncover hidden costs in your ELD and Fuel data.",
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
      <Hero />

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

    </main>
  );
}
