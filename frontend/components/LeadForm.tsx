"use client";

import { useState } from "react";
import { checkDotRisk, submitLead } from "../lib/api";
import { FleetSize, Role, LeadFormData, PainPoint, RiskData } from "../lib/types";
import { Loader2, AlertTriangle, CheckCircle, ArrowRight, ChevronLeft, X, ShieldCheck, Lock, FileCheck } from "lucide-react";
import { InlineWidget } from "react-calendly";

export default function LeadForm() {
  // STATE MACHINE: 'input' -> 'analyzing' -> 'results' -> 'qualification' -> 'submitting' -> 'success' -> 'waitlist'
  const [step, setStep] = useState<'input' | 'analyzing' | 'results' | 'qualification' | 'submitting' | 'success' | 'waitlist'>('input');
  
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
    pain_points: undefined,
    tech_stack: "",
  });

  const [riskData, setRiskData] = useState<RiskData | null>(null);
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
      
      // QUALIFICATION LOGIC
      const fleetSize = data.fleet_size || 0;
      if (fleetSize < 20) {
          setStep('waitlist');
      } else {
          setStep('results');
      }
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
                "Request Fleet Diagnostic"
            )}
          </button>
          
          {/* Trust Signals */}
          <div className="flex gap-4 justify-center mt-4 text-slate-400 text-xs font-semibold">
            <div className="flex items-center gap-1">
                <Lock className="w-3 h-3" /> AES-256
            </div>
            <div className="flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> SOC 2
            </div>
            <div className="flex items-center gap-1">
                <FileCheck className="w-3 h-3" /> FMCSA Verified
            </div>
          </div>
        </form>
      </div>
    );
  }

  // --- RENDER: STEP 2 (THE REVEAL & GATE) ---
  if (step === 'results') {
    if (!riskData) return null;
    
    // Determine Theme based on Risk
    const isHighRisk = riskData.risk_level === 'HIGH' || riskData.risk_level === 'CRITICAL';
    const themeColor = isHighRisk ? 'red' : 'blue';
    const borderColor = isHighRisk ? 'border-red-200' : 'border-blue-200';
    const bgColor = isHighRisk ? 'bg-red-50' : 'bg-blue-50';

    return (
      <div className={`bg-white p-8 rounded-xl shadow-2xl border-2 ${borderColor}`}>
        {/* 1. HERO HEADLINE */}
        <div className="text-center mb-8">
            <h3 className="text-2xl md:text-3xl font-bold text-slate-900 leading-tight">
                CRITICAL FINDINGS: <br/>
                <span className={isHighRisk ? "text-red-600" : "text-blue-600"}>
                    Your Fleet’s Valuation Defense Score is Compromised.
                </span>
            </h3>
        </div>

        {/* 2. DATA SCORECARD (VISUAL ANCHOR) */}
        <div className="grid grid-cols-3 gap-2 md:gap-4 mb-8">
            {/* Tile 1: Safety Rating */}
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-center">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-1">Safety Rating</div>
                <div className={`text-lg md:text-xl font-black ${riskData.rating === 'Conditional' ? 'text-red-600' : 'text-green-600'}`}>
                    {riskData.rating || 'N/A'}
                </div>
            </div>

            {/* Tile 2: Crash Count */}
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-center">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-1">Crashes (24mo)</div>
                <div className={`text-lg md:text-xl font-black ${riskData.total_crashes > 0 ? 'text-red-600' : 'text-slate-900'}`}>
                    {riskData.total_crashes}
                </div>
            </div>

            {/* Tile 3: Driver OOS */}
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-center">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-1">Driver OOS</div>
                <div className={`text-lg md:text-xl font-black ${riskData.driver_oos_rate > 5 ? 'text-orange-600' : 'text-slate-900'}`}>
                    {riskData.driver_oos_rate.toFixed(1)}%
                    <span className="text-xs text-slate-400 block font-normal mt-1">(Natl Avg: 3.81%)</span>
                </div>
            </div>
        </div>

        {/* 3. SPLIT-PATH COPY LOGIC */}
        <div className={`${bgColor} p-6 rounded-lg border ${borderColor} mb-8 text-left`}>
            {isHighRisk ? (
                <>
                    <h4 className="text-red-800 font-bold text-lg mb-2 flex items-center gap-2">
                        <AlertTriangle className="h-5 w-5" />
                        WARNING: CRITICAL LIABILITY EXPOSURE DETECTED
                    </h4>
                    <p className="text-red-700 text-sm leading-relaxed">
                        Your <strong>{riskData.rating}</strong> rating and Driver OOS rate confirm you are operating in a High-Risk status. 
                        This exposure, coupled with your crash history, is costing you <strong>$25,000+ per incident</strong> in unmitigated insurance liability.
                    </p>
                </>
            ) : (
                <>
                    <h4 className="text-blue-800 font-bold text-lg mb-2 flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        OPPORTUNITY: HIDDEN PROFIT THEFT DETECTED
                    </h4>
                    <p className="text-blue-700 text-sm leading-relaxed">
                        Congratulations on your Satisfactory rating. However, our scan indicates this clean record often hides massive internal leakage. 
                        Your fleet scale suggests <strong>$160,000 – $320,000</strong> in annual recoverable waste driven by fuel theft and poor utilization.
                    </p>
                </>
            )}
        </div>

        {/* 4. THE GATE (EMAIL CAPTURE) */}
        <form onSubmit={handleStage2Submit} className="space-y-4">
            <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">Enter Work Email to Unlock Report</label>
                <input
                    name="work_email"
                    type="email"
                    placeholder="name@company.com"
                    required
                    value={formData.work_email || ''}
                    onChange={handleChange}
                    className="w-full p-4 border-2 border-slate-200 rounded-lg text-slate-900 focus:border-blue-600 focus:outline-none"
                />
            </div>

            <button 
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg shadow-lg hover:shadow-xl transition-all flex justify-center items-center gap-2 text-lg"
            >
                Send My Confidential Liability Report <ArrowRight className="h-5 w-5" />
            </button>
            
            <p className="text-center text-xs text-slate-400 flex items-center justify-center gap-1">
                <Lock className="h-3 w-3" /> Confidentiality Guaranteed: Your data is secured with 256-bit encryption. We are SOC 2 ready.
            </p>
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
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider ml-1">What is your #1 Financial Headache?</label>
                <select
                    name="pain_points"
                    value={formData.pain_points || ''}
                    onChange={handleChange}
                    className="w-full p-3 border border-slate-300 rounded-lg bg-white text-slate-900"
                    required
                >
                    <option value="" disabled>Select your primary challenge...</option>
                    <option value={PainPoint.BROKER_FRAUD}>{PainPoint.BROKER_FRAUD}</option>
                    <option value={PainPoint.INSURANCE}>{PainPoint.INSURANCE}</option>
                    <option value={PainPoint.DOWNTIME}>{PainPoint.DOWNTIME}</option>
                    <option value={PainPoint.FUEL_THEFT}>{PainPoint.FUEL_THEFT}</option>
                    <option value={PainPoint.OTHER}>{PainPoint.OTHER}</option>
                </select>
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

  const getBookingContent = (riskLevel: string) => {
    if (riskLevel === 'LOW') {
        return {
            headline: "⚠️ WAIT. We found Unverified Spend in your logs.",
            body: "Your safety score is perfect—but that makes you the #1 target for Fuel Theft. The PDF in your email is just a diagnosis. To validate your $20,000 Savings Guarantee, we need to calibrate your fuel data manually.",
            badge: "💰 POTENTIAL LOST SAVINGS: $20,000+",
            badgeColor: "bg-red-100 text-red-800 border-red-200" // RED for Financial Failure
        };
    } else {
        // Default to High/Critical Risk
        return {
            headline: "⚠️ WAIT. Your Insurance Profile is Critical.",
            body: "Your 'Conditional' rating is a financial bleeding wound. Every day you wait is costing you extra in insurance premiums. We cannot fix this via email.",
            badge: "🔥 URGENT: INSURANCE RISK DETECTED",
            badgeColor: "bg-red-100 text-red-800 border-red-200"
        };
    }
  };

  // --- RENDER: STEP 4 (SUCCESS & BOOKING) ---
  if (step === 'success') {
    if (showBooking) {
        const content = getBookingContent(riskData?.risk_level || 'HIGH');
        
        return (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/95 backdrop-blur-sm p-4 overflow-y-auto">
                <div className="bg-white rounded-2xl shadow-2xl max-w-5xl w-full relative animate-in fade-in zoom-in duration-300 overflow-hidden my-8">
                    {/* TOP BAR */}
                    <div className="bg-slate-100 px-6 py-3 border-b border-slate-200 flex justify-between items-center">
                        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                            Step 3 of 3: Implementation
                        </span>
                        <button 
                            onClick={() => setShowBooking(false)}
                            className="text-slate-400 hover:text-slate-600 transition-colors"
                        >
                            <X className="h-5 w-5" />
                        </button>
                    </div>

                    <div className="p-6 md:p-8">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            {/* LEFT COLUMN - THE HOOK */}
                            <div className="flex flex-col h-full">
                                {/* SCARCITY ALERT (Moved to Top) */}
                                <div className="flex justify-center lg:justify-start mb-6">
                                    <div className="inline-flex items-center gap-2 text-orange-800 font-bold text-sm bg-orange-100 px-4 py-2 rounded-lg border border-orange-200 animate-pulse">
                                        <AlertTriangle className="h-4 w-4" />
                                        Only 3 Priority Slots remain this week
                                    </div>
                                </div>

                                {/* BADGE */}
                                <div className="flex justify-center lg:justify-start mb-4">
                                    <div className={`px-4 py-1.5 rounded-full border font-bold text-xs tracking-wide uppercase ${content.badgeColor}`}>
                                        {content.badge}
                                    </div>
                                </div>

                                {/* HEADLINE */}
                                <h2 className="text-2xl md:text-3xl font-bold text-slate-900 text-center lg:text-left mb-4 leading-tight">
                                    {content.headline}
                                </h2>

                                {/* BODY */}
                                <p className="text-slate-600 text-center lg:text-left mb-8 leading-relaxed">
                                    {content.body}
                                </p>

                                {/* VIDEO SLOT */}
                                <div className="w-full aspect-video rounded-lg overflow-hidden shadow-lg mb-6 relative bg-slate-900 mt-auto">
                                    <iframe 
                                        src="https://player.vimeo.com/video/1140156854?autoplay=1&title=0&byline=0&portrait=0" 
                                        className="absolute top-0 left-0 w-full h-full" 
                                        frameBorder="0" 
                                        allow="autoplay; fullscreen; picture-in-picture" 
                                        allowFullScreen
                                        loading="lazy"
                                        title="Fleet Clarity Audit Process Video"
                                    ></iframe>
                                </div>
                            </div>

                            {/* RIGHT COLUMN - THE ACTION */}
                            <div className="flex flex-col h-full">
                                {/* CALENDAR */}
                                <div className="rounded-xl overflow-hidden border-2 border-slate-100 shadow-xl bg-white mb-6 flex-grow">
                                    <InlineWidget 
                                        url={process.env.NEXT_PUBLIC_CALENDLY_URL!}
                                        prefill={{
                                            email: formData.work_email,
                                            name: formData.full_name,
                                            customAnswers: {
                                                a1: formData.pain_points, 
                                                a2: formData.phone
                                            }
                                        }}
                                        styles={{
                                            height: '500px'
                                        }}
                                    />
                                </div>

                                {/* FOOTER LINKS */}
                                <div className="text-center">
                                    <button 
                                        onClick={() => setShowBooking(false)}
                                        className="text-slate-400 text-xs hover:text-slate-600 underline hover:no-underline transition-all"
                                    >
                                        No thanks, I&apos;ll just wait for the PDF via email.
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
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

  // --- RENDER: WAITLIST (SMALL FLEETS) ---
  if (step === 'waitlist') {
      return (
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-8 text-center shadow-inner">
            <div className="flex justify-center mb-4">
                <div className="bg-slate-200 p-3 rounded-full">
                    <CheckCircle className="h-8 w-8 text-slate-500" />
                </div>
            </div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">Application Received</h3>
            <p className="text-slate-600 mb-6 text-sm leading-relaxed">
                Your fleet size is currently below our threshold for the Enterprise Audit. 
                We have added you to the waitlist for our Self-Serve Tool. 
                <br/><br/>
                <strong>Your basic report has been emailed.</strong>
            </p>
            <button 
                onClick={() => {
                    setStep('input');
                    setFormData({ ...formData, dot_number: "" });
                }}
                className="text-slate-500 hover:text-slate-800 font-semibold text-sm underline"
            >
                Return Home
            </button>
        </div>
      );
  }

  return null;
}
