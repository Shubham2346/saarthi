'use client'

import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { auth as authApi, users } from '@/lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch {
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const handleAuthResponse = useCallback((data) => {
    localStorage.setItem('token', data.access_token)
    if (data.refresh_token) {
      localStorage.setItem('refresh_token', data.refresh_token)
    }
    localStorage.setItem('user', JSON.stringify(data.user))
    setUser(data.user)
    return data.user
  }, [])

  const login = useCallback(async (idToken) => {
    try {
      setError(null)
      const data = await authApi.googleLogin(idToken)
      return handleAuthResponse(data)
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [handleAuthResponse])

  const emailLogin = useCallback(async (email, password) => {
    try {
      setError(null)
      const data = await authApi.emailLogin(email, password)
      return handleAuthResponse(data)
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [handleAuthResponse])

  const register = useCallback(async (email, password, name, role = 'student') => {
    try {
      setError(null)
      const data = await authApi.emailRegister(email, password, name, role)
      return handleAuthResponse(data)
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [handleAuthResponse])

  const forgotPassword = useCallback(async (email) => {
    try {
      setError(null)
      await authApi.forgotPassword(email)
      return true
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [])

  const resetPassword = useCallback(async (token, password) => {
    try {
      setError(null)
      await authApi.resetPassword(token, password)
      return true
    } catch (err) {
      setError(err.message)
      throw err
    }
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    setUser(null)
    setError(null)
  }, [])

  const refreshUser = useCallback(async () => {
    try {
      const userData = await users.me()
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
    } catch {
      logout()
    }
  }, [logout])

  return (
    <AuthContext.Provider value={{ 
      user, 
      loading, 
      error,
      login,
      emailLogin,
      register,
      forgotPassword,
      resetPassword,
      logout, 
      refreshUser 
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
