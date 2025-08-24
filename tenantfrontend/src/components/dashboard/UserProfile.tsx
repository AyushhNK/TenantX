"use client";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface UserProfileProps {
  user: User;
}

export default function UserProfile({ user }: UserProfileProps) {
  const displayName = user.first_name && user.last_name 
    ? `${user.first_name} ${user.last_name}`
    : user.username;

  return (
    <div className="flex items-center space-x-3">
      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
        <span className="text-white text-sm font-medium">
          {displayName.charAt(0).toUpperCase()}
        </span>
      </div>
      <div className="text-sm">
        <p className="font-medium text-gray-900">{displayName}</p>
        <p className="text-gray-500">{user.email}</p>
      </div>
    </div>
  );
} 