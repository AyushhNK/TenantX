"use client";

import { useState } from "react";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import LoginForm from "@/components/auth/LoginForm";
import SignupForm from "@/components/auth/SignupForm";
import Dashboard from "@/components/dashboard/Dashboard";

function HomeContent() {
  const [isLogin, setIsLogin] = useState(true);
  const { user, loading } = useAuth();

  console.log("HomeContent render - user:", user, "loading:", loading);

  if (loading) {
    console.log("Showing loading state");
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (user) {
    console.log("User is authenticated, showing dashboard");
    return <Dashboard />;
  }

  console.log("User is not authenticated, showing login/signup form");
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            TenantX
          </h1>
          <p className="text-lg text-gray-600">
            Multi-Tenant Platform for Organizations
          </p>
        </div>

        <div className="max-w-md mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex mb-6">
              <button
                onClick={() => setIsLogin(true)}
                className={`flex-1 py-2 px-4 rounded-l-lg font-medium transition-colors ${
                  isLogin
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                Login
              </button>
              <button
                onClick={() => setIsLogin(false)}
                className={`flex-1 py-2 px-4 rounded-r-lg font-medium transition-colors ${
                  !isLogin
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                Sign Up
              </button>
            </div>

            {isLogin ? <LoginForm /> : <SignupForm />}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <AuthProvider>
      <HomeContent />
    </AuthProvider>
  );
}
