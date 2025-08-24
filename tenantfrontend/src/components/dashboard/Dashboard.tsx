"use client";

import { useAuth } from "@/contexts/AuthContext";
import OrganizationSwitcher from "./OrganizationSwitcher";
import InviteMemberForm from "./InviteMemberForm";
import UserProfile from "./UserProfile";

export default function Dashboard() {
  const { user, organization, memberships, logout, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user || !organization) {
    return null; // This should not happen, but just in case
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">TenantX</h1>
              <div className="text-sm text-gray-500">
                {organization.name}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <UserProfile user={user} />
              <button
                onClick={logout}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg transition-colors duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Your Organizations
              </h2>
              <OrganizationSwitcher />
            </div>

            {memberships.some(m => m.role === "admin") && (
              <div className="bg-white rounded-lg shadow-md p-6 mt-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Invite Member
                </h2>
                <InviteMemberForm />
              </div>
            )}
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Welcome to {organization.name}
              </h2>
              <p className="text-gray-600 mb-4">
                You are currently viewing the dashboard for {organization.name}.
              </p>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium text-blue-900 mb-2">Your Role</h3>
                <p className="text-blue-800">
                  {memberships.find(m => m.organization.id === organization.id)?.role || "Member"}
                </p>
              </div>

              <div className="mt-6">
                <h3 className="font-medium text-gray-900 mb-3">Organization Details</h3>
                <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Name</dt>
                    <dd className="text-sm text-gray-900">{organization.name}</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Slug</dt>
                    <dd className="text-sm text-gray-900">{organization.slug}</dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Created</dt>
                    <dd className="text-sm text-gray-900">
                      {new Date(organization.created_at).toLocaleDateString()}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Memberships</dt>
                    <dd className="text-sm text-gray-900">{memberships.length}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 