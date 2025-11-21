"use client";

import { useState, useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { submitLead } from "../lib/api";
import { FleetSize, Role, LeadFormData } from "../lib/types";
import { Loader2, CheckCircle, AlertCircle } from "lucide-react";

export default function LeadForm() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Default State
  const [formData, setFormData] = useState<Partial<LeadFormData>>({
    fleet_size: undefined, // Force selection
    role: undefined,       // Force selection
    consent_audit: true,
    source: "landing_page",
    pain_points: "",
  });

  // Pain Points State for Multi-select
  const [selectedPainPoints, setSelectedPainPoints] = useState<string[]>([]);
  const [otherPainPoint, setOtherPainPoint] = useState("");

  const PAIN_POINT_OPTIONS = [
    "Fuel Fraud / Theft",
    "Unexpected Downtime",
    "Driver Retention",
    "High Insurance Costs",
    "Compliance / DOT Audits"
  ];

  // Capture UTMs on mount
  useEffect(() => {
    const utmSource = searchParams.get("utm_source");
    const utmCampaign = searchParams.get("utm_campaign");
    
    setFormData((prev) => ({
      ...prev,
      landing_page_path: pathname,
      utm_campaign: utmCampaign || undefined,
      source: utmSource || "landing_page",
    }));
  }, [pathname, searchParams]);

  // Update formData when pain points change
  useEffect(() => {
    const allPoints = [...selectedPainPoints];
    if (otherPainPoint.trim()) {
      allPoints.push(`Other: ${otherPainPoint}`);
    }
    setFormData(prev => ({ ...prev, pain_points: allPoints.join(", ") }));
  }, [selectedPainPoints, otherPainPoint]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const result = await submitLead(formData as LeadFormData);

    if (result.success) {
      setIsSuccess(true);
    } else {
      setError(result.error || "Submission failed");
    }
    setIsLoading(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePainPointToggle = (point: string) => {
    setSelectedPainPoints(prev => 
      prev.includes(point) 
        ? prev.filter(p => p !== point)
        : [...prev, point]
    );
  };

  const handleNextStep = () => {
    if (step === 1) {
      if (!formData.fleet_size || !formData.role || !formData.work_email) {
        setError("Please fill out all fields to continue.");
        return;
      }
      setError(null);
      setStep(2);
    }
  };

  if (isSuccess) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-8 text-center">
        <div className="flex justify-center mb-4">
          <CheckCircle className="h-12 w-12 text-green-600" />
        </div>
        <h3 className="text-xl font-bold text-green-800 mb-2">Request Received</h3>
        <p className="text-green-700">
          Your fleet data audit request has been queued. We will email you shortly to confirm your DOT verification.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-2xl border border-slate-100 relative overflow-hidden">
      {/* Progress Bar */}
      <div className="absolute top-0 left-0 w-full h-1 bg-slate-100">
        <div 
          className="h-full bg-blue-600 transition-all duration-500"
          style={{ width: step === 1 ? "50%" : "100%" }}
        />
      </div>

      <div className="mb-6 mt-2">
        <h3 className="text-2xl font-bold text-slate-900">
          {step === 1 ? "Get Your Fleet Audit" : "Finalize Your Request"}
        </h3>
        <p className="text-slate-500 text-sm">
          {step === 1 ? "See exactly where you're losing margin." : "Identify your top 3 hidden cost-per-mile leaks."}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm flex items-center gap-2 animate-pulse">
            <AlertCircle className="h-4 w-4" /> {error}
          </div>
        )}

        {step === 1 && (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider">Fleet Size</label>
              <select
                name="fleet_size"
                className="w-full p-3 border border-slate-300 rounded-lg bg-white text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.fleet_size || ""}
              >
                <option value="" disabled>Select Fleet Size</option>
                <option value={FleetSize.SMALL}>10-20 Trucks</option>
                <option value={FleetSize.MEDIUM}>21-50 Trucks</option>
                <option value={FleetSize.LARGE}>51-100 Trucks</option>
                <option value={FleetSize.ENTERPRISE}>100+ Trucks</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider">Your Role</label>
              <select
                name="role"
                className="w-full p-3 border border-slate-300 rounded-lg bg-white text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.role || ""}
              >
                <option value="" disabled>Select Your Role</option>
                <option value={Role.OWNER}>Owner / President</option>
                <option value={Role.MANAGER}>Fleet Manager</option>
                <option value={Role.OPS}>Operations</option>
                <option value={Role.FINANCE}>Finance</option>
                <option value={Role.OTHER}>Other</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider">Work Email</label>
              <input
                name="work_email"
                type="email"
                required
                placeholder="name@company.com"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.work_email || ""}
              />
            </div>

            <button
              type="button"
              onClick={handleNextStep}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg transition-all flex justify-center items-center gap-2 shadow-lg shadow-blue-600/20"
            >
              Next Step <Loader2 className="h-4 w-4 opacity-0" /> {/* Spacer */}
            </button>
            
            <p className="text-center text-xs text-slate-400">
              Step 1 of 2 • No credit card required
            </p>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="grid grid-cols-1 gap-4">
              <input
                name="full_name"
                required
                placeholder="Full Name"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.full_name || ""}
              />
              <input
                name="company_name"
                required
                placeholder="Company Name"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.company_name || ""}
              />
            </div>

            <div>
              <input
                name="dot_number"
                placeholder="DOT Number (Optional)"
                className="w-full p-3 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-blue-600 focus:outline-none"
                onChange={handleChange}
                value={formData.dot_number || ""}
              />
              <p className="text-xs text-slate-400 mt-1 ml-1">Helps us pre-qualify your fleet size instantly.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">Biggest Headaches (Select all that apply)</label>
              <div className="space-y-2">
                {PAIN_POINT_OPTIONS.map((point) => (
                  <label key={point} className="flex items-center gap-3 p-3 border border-slate-200 rounded-lg hover:bg-slate-50 cursor-pointer transition-colors">
                    <input
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                      checked={selectedPainPoints.includes(point)}
                      onChange={() => handlePainPointToggle(point)}
                    />
                    <span className="text-sm text-slate-700">{point}</span>
                  </label>
                ))}
                <input
                  placeholder="Other..."
                  className="w-full p-2 text-sm border-b border-slate-200 text-slate-900 focus:border-blue-500 focus:outline-none mt-2"
                  value={otherPainPoint}
                  onChange={(e) => setOtherPainPoint(e.target.value)}
                />
              </div>
            </div>

            <div className="flex items-start gap-2 bg-slate-50 p-3 rounded-lg">
              <input
                type="checkbox"
                name="consent_audit"
                checked={formData.consent_audit || false}
                className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300"
                onChange={(e) => setFormData(prev => ({...prev, consent_audit: e.target.checked}))}
              />
              <label className="text-xs text-slate-500 leading-relaxed">
                I agree to receive the audit report and related insights via email. We respect your inbox.
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-900 hover:bg-blue-800 text-white font-bold py-4 rounded-lg transition-all flex justify-center items-center gap-2 shadow-xl shadow-blue-900/20"
            >
              {isLoading ? <Loader2 className="animate-spin" /> : "Get My Free Profit Leak Report"}
            </button>
            
            <div className="flex justify-between items-center">
              <button 
                type="button" 
                onClick={() => setStep(1)}
                className="text-xs text-slate-400 hover:text-slate-600"
              >
                ← Back
              </button>
              <p className="text-xs text-red-500 font-medium animate-pulse">
                Only 5 slots left for this month
              </p>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
