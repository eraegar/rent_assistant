import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../stores/useAuthStore';
import { UserStatus } from '../types';

interface ProtectedRouteProps {
  requiredStatus: UserStatus;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ requiredStatus }) => {
  const { userStatus } = useAuthStore();

  if (userStatus === requiredStatus) {
    return <Outlet />;
  }

  // Redirect logic
  if (userStatus === UserStatus.UNAUTHENTICATED) {
    return <Navigate to="/" replace />;
  } else if (userStatus === UserStatus.NEEDS_SUBSCRIPTION) {
    // If already on payment screen, don't redirect again
    if (window.location.pathname !== '/payment') {
      return <Navigate to="/payment" replace />;
    }
  } else if (userStatus === UserStatus.HAS_ACTIVE_SUBSCRIPTION && requiredStatus !== UserStatus.HAS_ACTIVE_SUBSCRIPTION) {
    // If user has active subscription but tries to access a screen for non-subscribers
    return <Navigate to="/dashboard" replace />;
  }

  // Fallback, should ideally not be reached
  return <Navigate to="/" replace />;
};

export default ProtectedRoute; 