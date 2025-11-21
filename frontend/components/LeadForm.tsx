"use client";

import { useState, useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { submitLead } from "@/lib/api";
import { FleetSize, Role, LeadFormData } from "@/lib/types";
import { Loader2, CheckCircle, AlertCircle } from "lucide-react";

export default function LeadForm() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Default State
  const [formData, setFormData] = useState<Partial<LeadFormData>>({
    fleet_size: FleetSize.MEDIUM, // Default to target demographic
    role: Role.OWNER,
    consent_audit: true,
    source: "landing_page",
  });

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
    <div className="bg-white p-6 rounded-xl shadow-2xl border border-slate-100">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-slate-900">Get Your Fleet Audit</h3>
        <p className="text-slate-500 text-sm">See exactly where you&apos;re losing margin.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm flex items-center gap-2">
            <AlertCircle className="h-4 w-4" /> {error}
          </div>
        )}

        <div className="grid grid-cols-1 gap-4">
          <input
            name="full_name"
            required
            placeholder="Full Name"
            className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:outline-none"
            onChange={handleChange}
          />
          <input
            name="work_email"
            type="email"
            required
            placeholder="Work Email"
            className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:outline-none"
            onChange={handleChange}
          />
        </div>

        <input
          name="company_name"
          required
          placeholder="Company Name"
          className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:outline-none"
          onChange={handleChange}
        />

        {/* High Value Field: DOT Number */}
        <div>
          <input
            name="dot_number"
            placeholder="DOT Number (Optional)"
            className="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:outline-none"
            onChange={handleChange}
          />
          <p className="text-xs text-slate-400 mt-1 ml-1">Helps us pre-qualify your fleet size instantly.</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <select
            name="fleet_size"
            className="w-full p-3 border border-slate-300 rounded-lg bg-white"
            onChange={handleChange}
            defaultValue={FleetSize.MEDIUM}
          >
            <option value={FleetSize.SMALL}>10-20 Trucks</option>
            <option value={FleetSize.MEDIUM}>21-50 Trucks</option>
            <option value={FleetSize.LARGE}>51-100 Trucks</option>
            <option value={FleetSize.ENTERPRISE}>100+ Trucks</option>
          </select>

          <select
            name="role"
            className="w-full p-3 border border-slate-300 rounded-lg bg-white"
            onChange={handleChange}
            defaultValue={Role.OWNER}
          >
            <option value={Role.OWNER}>Owner / President</option>
            <option value={Role.MANAGER}>Fleet Manager</option>
            <option value={Role.OPS}>Operations</option>
            <option value={Role.FINANCE}>Finance</option>
            <option value={Role.OTHER}>Other</option>
          </select>
        </div>

        <textarea
          name="pain_points"
          placeholder="What is your biggest headache? (e.g. Fuel theft, Breakdowns...)"
          className="w-full p-3 border border-slate-300 rounded-lg h-24 focus:ring-2 focus:ring-blue-600 focus:outline-none"
          onChange={handleChange}
        />

        <div className="flex items-start gap-2">
          <input
            type="checkbox"
            name="consent_audit"
            defaultChecked={true}
            className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300"
            onChange={(e) => setFormData(prev => ({...prev, consent_audit: e.target.checked}))}
          />
          <label className="text-xs text-slate-500">
            I agree to receive the audit report and related insights via email.
          </label>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-900 hover:bg-blue-800 text-white font-bold py-4 rounded-lg transition-all flex justify-center items-center gap-2"
        >
          {isLoading ? <Loader2 className="animate-spin" /> : "Book Data Audit"}
        </button>
      </form>
    </div>
  );
}
