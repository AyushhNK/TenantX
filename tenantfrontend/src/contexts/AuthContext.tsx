"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface Organization {
  id: number;
  name: string;
  slug: string;
  created_at: string;
}

interface Membership {
  organization: Organization;
  role: string;
  joined_at: string;
}

interface AuthContextType {
  user: User | null;
  organization: Organization | null;
  memberships: Membership[];
  accessToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => void;
  switchOrganization: (orgId: number) => Promise<void>;
  inviteMember: (orgId: number, email: string, role: string) => Promise<void>;
  loading: boolean;
}

interface SignupData {
  org_name: string;
  org_slug?: string;
  email: string;
  username: string;
  password: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [memberships, setMemberships] = useState<Membership[]>([]);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = "http://localhost:8000/api/accounts";

  useEffect(() => {
    // Check for stored token on app load
    const token = localStorage.getItem("accessToken");
    if (token) {
      setAccessToken(token);
      fetchUserProfile(token);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserProfile = async (token: string) => {
    try {
      console.log("Fetching user profile with token...");
      // First, get user data
      const userResponse = await fetch(`${API_BASE_URL}/me/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        console.log("User data received:", userData);
        setUser(userData);
      } else {
        console.error("Failed to fetch user data:", userResponse.status);
      }

      // Then, get memberships
      const membershipsResponse = await fetch(`${API_BASE_URL}/me/memberships/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (membershipsResponse.ok) {
        const membershipsData = await membershipsResponse.json();
        console.log("Memberships data received:", membershipsData);
        setMemberships(membershipsData);
        if (membershipsData.length > 0) {
          setOrganization(membershipsData[0].organization);
        }
      } else {
        console.error("Failed to fetch memberships:", membershipsResponse.status);
        // Token might be expired
        localStorage.removeItem("accessToken");
        setAccessToken(null);
        setUser(null);
        setOrganization(null);
        setMemberships([]);
      }
    } catch (error) {
      console.error("Error fetching user profile:", error);
      // Clear everything on error
      localStorage.removeItem("accessToken");
      setAccessToken(null);
      setUser(null);
      setOrganization(null);
      setMemberships([]);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      console.log("Attempting login...");
      const response = await fetch(`${API_BASE_URL}/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Login successful, tokens received:", data);
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);
        setAccessToken(data.access);
        
        // Fetch user profile and memberships
        console.log("Fetching user profile...");
        await fetchUserProfile(data.access);
      } else {
        const errorData = await response.json();
        console.error("Login failed:", errorData);
        throw new Error(errorData.error || "Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const signup = async (data: SignupData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const responseData = await response.json();
        localStorage.setItem("accessToken", responseData.access);
        localStorage.setItem("refreshToken", responseData.refresh);
        setAccessToken(responseData.access);
        setUser(responseData.user);
        setOrganization(responseData.organization);
        setMemberships([{
          organization: responseData.organization,
          role: "admin",
          joined_at: new Date().toISOString(),
        }]);
      } else {
        const errorData = await response.json();
        throw new Error(Object.values(errorData).flat().join(", "));
      }
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
    setOrganization(null);
    setMemberships([]);
    setAccessToken(null);
  };

  const switchOrganization = async (orgId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/switch-org/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ org_id: orgId }),
      });

      if (response.ok) {
        const membership = memberships.find(m => m.organization.id === orgId);
        if (membership) {
          setOrganization(membership.organization);
        }
      } else {
        throw new Error("Failed to switch organization");
      }
    } catch (error) {
      throw error;
    }
  };

  const inviteMember = async (orgId: number, email: string, role: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/organizations/${orgId}/invite/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ email, role }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to invite member");
      }
    } catch (error) {
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    organization,
    memberships,
    accessToken,
    login,
    signup,
    logout,
    switchOrganization,
    inviteMember,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 