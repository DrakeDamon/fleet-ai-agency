import { Check, ShieldCheck, Lock, FileCheck } from "lucide-react";
import LeadForm from "./LeadForm";

export default function Hero() {
  return (
    <section className="relative bg-slate-900 text-white pt-20 pb-32 overflow-hidden">
      <div className="container mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
        <div className="z-10">
          <div className="inline-block bg-blue-600/20 text-blue-300 px-3 py-1 rounded-full text-sm font-semibold mb-6 border border-blue-500/30">
            For Fleets with 20–100 Power Units
          </div>
          <h1 className="text-4xl lg:text-5xl font-bold leading-tight mb-6">
            STOP Funding Fleet Failure: Instantly Quantify the Hidden <span className="text-red-400">$250K Corporate Liability</span> in Your Operational Data.
          </h1>
          <p className="text-lg text-slate-300 mb-8 max-w-lg leading-relaxed">
            Generic telematics stops at data. We deploy proprietary AI anomaly detection models to expose systemic fraud and utilization loss, guaranteeing actionable profit recovery. The $7,500 Forensic Audit is the mandatory first step to restore financial control and begin risk mitigation.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 mb-8">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all text-lg">
                Request Fleet Diagnostic
            </button>
          </div>

          {/* Trust Signals */}
          <div className="flex flex-wrap gap-6 items-center text-slate-500 text-sm font-semibold">
            <div className="flex items-center gap-2">
                <Lock className="w-4 h-4" /> AES-256 Encryption
            </div>
            <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4" /> SOC 2 Architecture
            </div>
            <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4" /> FMCSA Verified
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-slate-800">
             <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider mb-3">Trusted By Fleets Using</p>
              <div className="flex flex-wrap gap-6 opacity-60 grayscale text-slate-400 font-bold text-lg items-center">
                <span>Samsara</span>
                <span>Motive</span>
                <span>Geotab</span>
                <span>Omnitracs</span>
              </div>
          </div>
        </div>
        
        <div className="z-10">
          <LeadForm />
          {/* Testimonial */}
          <div className="mt-6 bg-slate-800/50 p-4 rounded-lg border border-slate-700 backdrop-blur-sm">
            <div className="flex gap-1 text-yellow-400 mb-2">
              {"★★★★★"}
            </div>
            <p className="text-slate-300 text-sm italic">
              &quot;We found $80K in fuel fraud within the first week of the audit. It paid for itself 10x over.&quot;
            </p>
            <p className="text-slate-500 text-xs mt-2 font-semibold">
              — Mike T., Fleet Operations Director
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
