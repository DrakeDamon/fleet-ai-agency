import { LeadFormData, ApiError } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function submitLead(data: LeadFormData): Promise<{ success: boolean; error?: string }> {
  try {
    const response = await fetch(`${API_URL}/api/v1/leads/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      return { success: true };
    }

    // Handle specific error codes
    if (response.status === 429) {
      return { success: false, error: "Too many submissions. Please wait 60 seconds and try again." };
    }

    if (response.status === 422) {
      return { success: false, error: "Please check your inputs. Valid email and fleet size are required." };
    }

    // Generic fallback
    return { success: false, error: "Something went wrong. Please try again later." };
  } catch (error) {
    console.error("API Error:", error);
    return { success: false, error: "Network error" };
  }
}

export async function checkDotRisk(dotNumber: string) {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/leads/audit/preview/${dotNumber}`);
    if (!res.ok) throw new Error("DOT Not Found");
    return await res.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}
