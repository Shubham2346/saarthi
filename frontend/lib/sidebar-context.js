'use client'

import { createContext, useContext, useState, useCallback } from 'react'

const SidebarContext = createContext(null)

export function SidebarProvider({ children }) {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const toggleCollapsed = useCallback(() => {
    setCollapsed(prev => !prev)
  }, [])

  const openMobile = useCallback(() => {
    setMobileOpen(true)
    document.body.style.overflow = 'hidden'
  }, [])

  const closeMobile = useCallback(() => {
    setMobileOpen(false)
    document.body.style.overflow = ''
  }, [])

  return (
    <SidebarContext.Provider value={{
      collapsed,
      mobileOpen,
      toggleCollapsed,
      openMobile,
      closeMobile,
    }}>
      {children}
    </SidebarContext.Provider>
  )
}

export function useSidebar() {
  const ctx = useContext(SidebarContext)
  if (!ctx) throw new Error('useSidebar must be used inside SidebarProvider')
  return ctx
}
