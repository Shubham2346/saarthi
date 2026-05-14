'use client'

import { usePathname } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { useTheme } from '@/lib/theme'
import { useSidebar } from '@/lib/sidebar-context'
import { cn } from '@/lib/utils'
import { ROLE_LABELS, ROLE_COLORS } from '@/lib/roles'
import {
  PanelLeft, Search, Bell, Sun, Moon, ChevronRight, Home,
  ChevronDown, LogOut, User, Settings
} from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

function Breadcrumbs() {
  const pathname = usePathname()
  const segments = pathname.split('/').filter(Boolean)

  return (
    <nav className="hidden sm:flex items-center gap-1.5 text-xs text-muted-foreground" aria-label="Breadcrumb">
      <Home className="w-3.5 h-3.5" />
      {segments.map((seg, i) => (
        <span key={i} className="flex items-center gap-1.5">
          <ChevronRight className="w-3 h-3" />
          <span className={cn('capitalize', i === segments.length - 1 && 'text-foreground font-semibold')}>
            {seg.replace(/-/g, ' ')}
          </span>
        </span>
      ))}
    </nav>
  )
}

function NotificationBell() {
  return (
    <button className="relative p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-all duration-200" aria-label="Notifications">
      <Bell className="w-5 h-5" />
      <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full animate-ping-subtle" />
      <span className="sr-only">3 unread notifications</span>
    </button>
  )
}

function ProfileDropdown() {
  const { user, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 pl-2 border-l border-border group"
        aria-label="Profile menu"
        aria-expanded={open}
      >
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 ring-2 ring-background group-hover:ring-indigo-300 dark:group-hover:ring-indigo-700 transition-all">
          {user?.full_name?.[0] || user?.email?.[0] || '?'}
        </div>
        <div className="hidden lg:block text-left">
          <p className="text-sm font-medium text-foreground leading-tight">{user?.full_name || 'User'}</p>
          <p className="text-[10px] text-muted-foreground">{ROLE_LABELS[user?.role] || user?.role}</p>
        </div>
        <ChevronDown className="hidden lg:block w-3.5 h-3.5 text-muted-foreground transition-transform duration-200" style={{ transform: open ? 'rotate(180deg)' : 'rotate(0)' }} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full mt-2 w-56 rounded-xl border border-border bg-popover shadow-elevated p-1.5 z-50"
          >
            <div className="px-3 py-2 mb-1 border-b border-border">
              <p className="text-sm font-medium text-foreground">{user?.full_name || 'User'}</p>
              <p className="text-xs text-muted-foreground">{user?.email || ''}</p>
            </div>
            <button className="flex items-center gap-2.5 w-full px-3 py-2 rounded-lg text-sm text-foreground hover:bg-accent transition-colors">
              <User className="w-4 h-4" /> Profile
            </button>
            <button className="flex items-center gap-2.5 w-full px-3 py-2 rounded-lg text-sm text-foreground hover:bg-accent transition-colors">
              <Settings className="w-4 h-4" /> Settings
            </button>
            <div className="border-t border-border mt-1 pt-1">
              <button
                onClick={() => { logout(); setOpen(false) }}
                className="flex items-center gap-2.5 w-full px-3 py-2 rounded-lg text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors"
              >
                <LogOut className="w-4 h-4" /> Sign Out
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function TopNavbar() {
  const { user } = useAuth()
  const { toggleCollapsed, openMobile } = useSidebar()
  const { theme, toggleTheme } = useTheme()
  const role = user?.role || 'student'
  const roleColors = ROLE_COLORS[role] || {}

  return (
    <header className="h-16 flex-shrink-0 border-b border-border bg-background/80 backdrop-blur-xl sticky top-0 z-30">
      <div className="flex items-center justify-between h-full px-4 lg:px-6">
        <div className="flex items-center gap-3">
          {/* Mobile hamburger */}
          <button
            onClick={openMobile}
            className="p-2 -ml-2 rounded-lg hover:bg-accent transition-colors lg:hidden"
            aria-label="Open navigation menu"
          >
            <PanelLeft className="w-5 h-5 text-foreground" />
          </button>

          {/* Desktop hamburger */}
          <button
            onClick={toggleCollapsed}
            className="hidden lg:flex p-2 -ml-2 rounded-lg hover:bg-accent transition-colors"
            aria-label="Toggle sidebar"
          >
            <PanelLeft className="w-5 h-5 text-foreground" />
          </button>

          <Breadcrumbs />
        </div>

        <div className="flex items-center gap-2">
          {/* Search */}
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search..."
              className="w-64 h-9 pl-9 pr-3 rounded-lg border border-input bg-background text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring/30 transition-all"
              aria-label="Search"
            />
          </div>

          {/* Role badge */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-accent/50">
            <span className={cn('w-1.5 h-1.5 rounded-full', roleColors.dot)} />
            <span className="text-xs font-medium text-muted-foreground">{ROLE_LABELS[role] || role}</span>
          </div>

          <NotificationBell />

          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-all duration-200"
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          <ProfileDropdown />
        </div>
      </div>
    </header>
  )
}
