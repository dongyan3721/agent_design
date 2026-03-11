"use client";

import { useCallback, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuthStore } from "@/stores";
import { apiClient, ApiError } from "@/lib/api-client";
import type { User, LoginRequest, RegisterRequest } from "@/types";
import { ROUTES, extractLocaleFromPathname, withLocale } from "@/lib/constants";

export function useAuth() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = extractLocaleFromPathname(pathname);
  const { user, isAuthenticated, isLoading, setUser, setLoading, logout } =
    useAuthStore();

  // Check auth status on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await apiClient.get<User>("/auth/me");
        setUser(userData);
      } catch {
        setUser(null);
      }
    };

    if (isLoading) {
      checkAuth();
    }
  }, [isLoading, setUser]);

  const login = useCallback(
    async (credentials: LoginRequest) => {
      setLoading(true);
      try {
        const response = await apiClient.post<{ user: User; message: string }>(
          "/auth/login",
          credentials
        );
        setUser(response.user);
        router.push(withLocale(ROUTES.DASHBOARD, locale));
        return response;
      } catch (error) {
        setLoading(false);
        throw error;
      }
    },
    [locale, router, setUser, setLoading]
  );

  const register = useCallback(
    async (data: RegisterRequest) => {
      const response = await apiClient.post<{ id: string; email: string }>(
        "/auth/register",
        data
      );
      return response;
    },
    []
  );

  const handleLogout = useCallback(async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch {
      // Ignore logout errors
    } finally {
      logout();
      router.push(withLocale(ROUTES.LOGIN, locale));
    }
  }, [locale, logout, router]);

  const refreshToken = useCallback(async () => {
    try {
      await apiClient.post("/auth/refresh");
      // Re-fetch user after token refresh
      const userData = await apiClient.get<User>("/auth/me");
      setUser(userData);
      return true;
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        logout();
        router.push(withLocale(ROUTES.LOGIN, locale));
      }
      return false;
    }
  }, [locale, logout, router, setUser]);

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout: handleLogout,
    refreshToken,
  };
}
