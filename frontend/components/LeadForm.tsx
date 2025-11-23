"use client";

import { useState } from "react";
import { checkDotRisk, submitLead } from "../lib/api";
import { FleetSize, Role, LeadFormData } from "../lib/types";
import { Loader2, AlertTriangle, CheckCircle, ArrowRight, ChevronLeft } from "lucide-react";
import { InlineWidget } from "react-calendly";

export default function LeadForm() {
  // STATE MACHINE: 'input' -> 'analyzing' -> 'results' -> 'qualification' -> 'submitting' -> 'success'
  const [step, setStep] = useState<'input' | 'analyzing' | 'results' | 'qualification' | 'submitting' | 'success'>('input');
  
  // SINGLE SOURCE OF TRUTH
  const [formData, setFormData] = useState<Partial<LeadFormData>>({
    dot_number: "",
    full_name: "",
    work_email: "",
    company_name: "",
    fleet_size: undefined,
    role: undefined,
    consent_audit: true,
    phone: "",
    pain_points: "",
    tech_stack: "",
  });

  const [riskData, setRiskData] = useState<any>(null);
  const [showBooking, setShowBooking] = useState(true);

  // HANDLERS
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const runInstantAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.dot_number) return;
    
    setStep('analyzing');
    // Simulate "Calculating" delay for effect (psychology)
    await new Promise(r => setTimeout(r, 1500));
    
    const data = await checkDotRisk(formData.dot_number);
    if (data) {
      setRiskData(data);
      setFormData(prev => ({ ...prev, company_name: data.company_name })); // Auto-fill Name
      setStep('results');
    } else {
      // Fallback if DOT not found
      setStep('input'); 
      alert("DOT Number not found. Please check and try again.");
    }
  };

  const handleStage2Submit = (e: React.FormEvent) => {
    e.preventDefault();
    // Basic validation
    if (!formData.full_name || !formData.work_email || !formData.fleet_size || !formData.role) {
        alert("Please fill in all fields to proceed.");
        return;
    }
    setStep('qualification');
  };

  const submitFinalLead = async (e: React.FormEvent) => {
    e.preventDefault();
    setStep('submitting');
    // Combine the Risk Data into the "Pain Points" field for your reference
    const finalPayload = {
        ...formData,
        pain_points: `User Input: ${formData.pain_points} | Auto-Audit Risk: ${riskData?.risk_level} | Flags: ${riskData?.risk_flags?.join(", ")}`
    };
    
    await submitLead(finalPayload as LeadFormData);
    setStep('success');
  };

  // --- RENDER: STEP 1 (THE HOOK) ---
  if (step === 'input' || step === 'analyzing') {
    return (
      <div className="bg-white p-8 rounded-xl shadow-2xl border border-slate-200">
        <div className="mb-6 text-center">
            <span className="bg-red-100 text-red-700 text-xs font-bold px-2 py-1 rounded-full uppercase tracking-wide">
                Free Tool
            </span>
            <h3 className="text-2xl font-bold text-slate-900 mt-3">
                Check Your DOT Risk Score
            </h3>
            <p className="text-slate-500 text-sm mt-2">
                Enter your DOT# to see if you are flagged for an audit.
            </p>
        </div>

        <form onSubmit={runInstantAudit} className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">US DOT Number</label>
            <input
                name="dot_number"
                placeholder="e.g. 1234567"
                value={formData.dot_number || ''} // SINGLE SOURCE OF TRUTH
                onChange={handleChange}
                className="w-full p-4 text-lg border-2 border-slate-200 rounded-lg text-slate-900 focus:border-blue-600 focus:outline-none font-mono"
                required
            />
          </div>

          <button 
            disabled={step === 'analyzing'}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg transition-all flex justify-center items-center gap-2 text-lg"
          >
            {step === 'analyzing' ? (
                <><Loader2 className="animate-spin" /> Analyzing FMCSA Database...</>
            ) : (
                "Check My Risk Score"
            )}
          </button>
        </form>
      </div>
    );
  }

  // --- RENDER: STEP 2 (THE TEASER & GATE) ---
  if (step === 'results') {
    return (
      <div className="bg-white p-8 rounded-xl shadow-2xl border-2 border-red-100">
        {/* TEASER RESULTS */}
        <div className="text-center mb-6">
            <div className="inline-flex items-center gap-2 text-red-600 font-bold text-xl mb-2">
                <AlertTriangle className="h-6 w-6" />
                {riskData.risk_level} RISK DETECTED
            </div>
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-left space-y-2">
                <p className="text-sm text-slate-600">
                    <strong>Fleet:</strong> {riskData.company_name}
                </p>
                <p className="text-sm text-slate-600">
                    <strong>Vehicle OOS:</strong> <span className="text-red-600 font-bold">{riskData.vehicle_oos_rate}%</span> 
                    <span className="text-slate-400 text-xs ml-1">(Natl Avg: 22%)</span>
                </p>
                <p className="text-xs text-slate-500 mt-2 italic">
                    We found {riskData.risk_flags.length} critical data errors triggering this score.
                </p>
            </div>
        </div>

        {/* THE GATE FORM */}
        <form onSubmit={handleStage2Submit} className="space-y-3">
            <h4 className="text-md font-bold text-slate-800 text-center">
                Where should we send the Fix Report?
            </h4>
            
            <input
                name="full_name"
                placeholder="Your Name"
                required
                value={formData.full_name || ''}
                onChange={handleChange}
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900"
            />
            <input
                name="work_email"
                type="email"
                placeholder="Work Email (Required for Report)"
                required
                value={formData.work_email || ''}
                onChange={handleChange}
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900"
            />
            
            <div className="grid grid-cols-2 gap-2">
                <select 
                    name="fleet_size" 
                    value={formData.fleet_size || ''} 
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg bg-white text-slate-900"
                    required
                >
                    <option value="" disabled>Fleet Size</option>
                    <option value={FleetSize.SMALL}>10-20 Trucks</option>
                    <option value={FleetSize.MEDIUM}>21-50 Trucks</option>
                    <option value={FleetSize.LARGE}>51-100 Trucks</option>
                    <option value={FleetSize.ENTERPRISE}>100+ Trucks</option>
                </select>
                
                 <select 
                    name="role" 
                    value={formData.role || ''} 
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg bg-white text-slate-900"
                    required
                >
                    <option value="" disabled>Role</option>
                    <option value={Role.OWNER}>Owner</option>
                    <option value={Role.MANAGER}>Manager</option>
                    <option value={Role.FINANCE}>Finance</option>
                    <option value={Role.OTHER}>Other</option>
                </select>
            </div>

            <button 
                type="submit"
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-lg shadow-lg hover:shadow-xl transition-all flex justify-center items-center gap-2 mt-4"
            >
                Unlock My Full Report <ArrowRight/>
            </button>
        </form>
      </div>
    );
  }

  // --- RENDER: STEP 3 (QUALIFICATION) ---
  if (step === 'qualification' || step === 'submitting') {
    return (
      <div className="bg-white p-8 rounded-xl shadow-2xl border border-slate-200">
        <div className="mb-6 text-center">
            <h3 className="text-2xl font-bold text-slate-900">
                Final Step: Customize Your Audit
            </h3>
            <p className="text-slate-500 text-sm mt-2">
                To ensure your report is accurate, tell us a bit about your operations.
            </p>
        </div>

        <form onSubmit={submitFinalLead} className="space-y-4">
            <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">Mobile Number (For SMS Alerts)</label>
                <input
                    name="phone"
                    type="tel"
                    placeholder="(555) 555-5555"
                    value={formData.phone || ''}
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg text-slate-900"
                />
            </div>

            <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">What is your primary financial headache right now?</label>
                <textarea
                    name="pain_points"
                    placeholder="e.g. Fuel theft, Unplanned downtime, Broker fraud..."
                    value={formData.pain_points || ''}
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 h-24"
                    required
                />
            </div>

            <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">What ELD or TMS do you use?</label>
                <textarea
                    name="tech_stack"
                    placeholder="e.g. Samsara, Motive, McLeod..."
                    value={formData.tech_stack || ''}
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 h-20"
                />
            </div>

            <button 
                disabled={step === 'submitting'}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg shadow-lg hover:shadow-xl transition-all flex justify-center items-center gap-2 mt-2"
            >
                {step === 'submitting' ? <Loader2 className="animate-spin"/> : "Generate My Risk Report"}
            </button>
            
            <div className="text-center mt-4">
                <button 
                    type="button" 
                    onClick={() => setStep('results')}
                    className="text-slate-400 text-sm hover:text-slate-600 flex items-center justify-center gap-1 mx-auto"
                >
                    <ChevronLeft className="h-4 w-4" /> Back
                </button>
            </div>
        </form>
      </div>
    );
  }

  // --- RENDER: STEP 4 (SUCCESS & BOOKING) ---
  if (step === 'success') {
    if (showBooking) {
        return (
            <div className="bg-white p-6 rounded-xl shadow-2xl border-2 border-orange-200">
                <div className="text-center mb-4">
                    <div className="inline-flex items-center gap-2 text-orange-600 font-bold text-lg animate-pulse">
                        <AlertTriangle className="h-5 w-5" />
                        WAIT. Your Risk Score is Higher Than Average.
                    </div>
                    <p className="text-slate-600 text-sm mt-2">
                        Your Data Risk Snapshot has been sent to <strong>{formData.work_email}</strong>. 
                        However, due to your critical risk factors, we have unlocked a <span className="font-bold text-slate-900">Priority Review Call</span> to explain these findings immediately.
                    </p>
                </div>

                <div className="rounded-lg overflow-hidden border border-slate-200">
                    <InlineWidget 
                        url="https://calendly.com/drake-damon-fleet-ai/15min"
                        prefill={{
                            email: formData.work_email,
                            name: formData.full_name,
                            customAnswers: {
                                a1: formData.pain_points, // Assuming 'a1' maps to a question in your Calendly
                                a2: formData.phone
                            }
                        }}
                        styles={{
                            height: '450px'
                        }}
                    />
                </div>

                <div className="text-center mt-4">
                    <button 
                        onClick={() => setShowBooking(false)}
                        className="text-slate-400 text-xs hover:text-slate-600 underline"
                    >
                        No thanks, I'll just wait for the PDF via email.
                    </button>
                </div>
            </div>
        );
    }

    // STANDARD SUCCESS VIEW
    return (
        <div className="bg-green-50 border border-green-200 rounded-xl p-8 text-center">
            <div className="flex justify-center mb-4">
                <CheckCircle className="h-16 w-16 text-green-600" />
            </div>
            <h3 className="text-2xl font-bold text-green-800 mb-2">Report Generating...</h3>
            <p className="text-green-700">
                We are pulling your full FMCSA inspection history now. 
                Check your email in 5-10 minutes for your <strong>Data Risk Snapshot</strong>.
            </p>
        </div>
    );
  }

  return null;
}
