"use client";

import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export default function OrganizationSwitcher() {
  const { memberships, organization, switchOrganization } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleSwitch = async (orgId: number) => {
    if (orgId === organization?.id) return;
    
    setLoading(true);
    try {
      await switchOrganization(orgId);
    } catch (error) {
      console.error("Failed to switch organization:", error);
    } finally {
      setLoading(false);
    }
  };

  if (memberships.length === 0) {
    return (
      <div className="text-center py-4">
        <p className="text-gray-500">No organizations found</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {memberships.map((membership) => (
        <button
          key={membership.organization.id}
          onClick={() => handleSwitch(membership.organization.id)}
          disabled={loading}
          className={`w-full text-left p-3 rounded-lg border transition-colors ${
            organization?.id === membership.organization.id
              ? "bg-blue-50 border-blue-200 text-blue-900"
              : "bg-white border-gray-200 hover:bg-gray-50"
          } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-sm">
                {membership.organization.name}
              </h3>
              <p className="text-xs text-gray-500">
                {membership.organization.slug}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 text-xs rounded-full ${
                membership.role === "admin"
                  ? "bg-red-100 text-red-800"
                  : membership.role === "manager"
                  ? "bg-yellow-100 text-yellow-800"
                  : "bg-gray-100 text-gray-800"
              }`}>
                {membership.role}
              </span>
              {organization?.id === membership.organization.id && (
                <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
              )}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
} 