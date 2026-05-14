'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { useSidebar } from '@/lib/sidebar-context'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard, Sparkles, FileText, MessageCircle, CreditCard,
  CheckSquare, Users, LogOut, HelpCircle,
  Inbox, UserCog, BarChart3, BookOpen, Shield,
  ClipboardList, Calendar, TrendingUp, Bell,
  Terminal, Key, Activity, Database, FileCheck,
  ChevronLeft, ChevronRight, GraduationCap, School, Settings,
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

const NAV_CONFIG = {
  student: {
    label: 'Student',
    icon: GraduationCap,
    gradient: 'from-indigo-500 to-purple-600',
    items: [
      { key: 'dashboard', href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { key: 'admission', href: '/admission', label: 'Admission Progress', icon: Sparkles },
      { key: 'documents', href: '/documents', label: 'Documents', icon: FileText },
      { key: 'chat', href: '/chat', label: 'AI Assistant', icon: MessageCircle },
      { key: 'tasks', href: '/tasks', label: 'My Tasks', icon: CheckSquare },
      { key: 'payment', href: '/payment', label: 'Payments', icon: CreditCard },
    ],
  },
  admin: {
    label: 'Admin',
    icon: Shield,
    gradient: 'from-blue-500 to-cyan-600',
    items: [
      { key: 'dashboard', href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
      { key: 'applications', href: '/admin/applications', label: 'Applications', icon: Inbox },
      { key: 'students', href: '/admin/students', label: 'Student Management', icon: Users },
      { key: 'documents', href: '/admin/documents', label: 'Verification Queue', icon: FileCheck, badge: '12' },
      { key: 'analytics', href: '/admin/analytics', label: 'Analytics', icon: BarChart3 },
      { key: 'knowledge', href: '/admin/knowledge', label: 'Knowledge Base', icon: BookOpen },
      { key: 'tickets', href: '/admin/tickets', label: 'Support Tickets', icon: Bell },
      { key: 'mentors', href: '/admin/mentors', label: 'Mentor Management', icon: UserCog },
    ],
  },
  department_coordinator: {
    label: 'Coordinator',
    icon: ClipboardList,
    gradient: 'from-emerald-500 to-teal-600',
    items: [
      { key: 'dashboard', href: '/coordinator', label: 'Dashboard', icon: LayoutDashboard },
      { key: 'students', href: '/coordinator/students', label: 'Department Students', icon: Users },
      { key: 'applications', href: '/coordinator/applications', label: 'Applications', icon: Inbox, badge: '5' },
      { key: 'reports', href: '/coordinator/reports', label: 'Reports', icon: BarChart3 },
    ],
  },
  mentor: {
    label: 'Mentor',
    icon: Users,
    gradient: 'from-amber-500 to-orange-600',
    items: [
      { key: 'dashboard', href: '/mentor', label: 'Dashboard', icon: LayoutDashboard },
      { key: 'students', href: '/mentor/students', label: 'Assigned Students', icon: Users },
      { key: 'schedule', href: '/mentor/schedule', label: 'Meetings', icon: Calendar },
      { key: 'notes', href: '/mentor/notes', label: 'Mentor Notes', icon: FileText },
    ],
  },
  system_admin: {
    label: 'System Admin',
    icon: Terminal,
    gradient: 'from-rose-500 to-pink-600',
    items: [
      { key: 'overview', href: '/system-admin', label: 'System Overview', icon: LayoutDashboard },
      { key: 'users', href: '/system-admin/users', label: 'Users', icon: Users },
      { key: 'roles', href: '/system-admin/roles', label: 'Roles & Permissions', icon: Key },
      { key: 'audit', href: '/system-admin/audit', label: 'Audit Logs', icon: ClipboardList },
      { key: 'monitoring', href: '/system-admin/monitoring', label: 'System Health', icon: Activity },
      { key: 'settings', href: '/system-admin/settings', label: 'Platform Settings', icon: Settings },
    ],
  },
}

const roleGradients = {
  student: { bg: 'from-indigo-500 to-purple-600', text: 'text-indigo-600 dark:text-indigo-400', activeBg: 'bg-indigo-50 dark:bg-indigo-500/10', activeBar: 'bg-indigo-500' },
  admin: { bg: 'from-blue-500 to-cyan-600', text: 'text-blue-600 dark:text-blue-400', activeBg: 'bg-blue-50 dark:bg-blue-500/10', activeBar: 'bg-blue-500' },
  department_coordinator: { bg: 'from-emerald-500 to-teal-600', text: 'text-emerald-600 dark:text-emerald-400', activeBg: 'bg-emerald-50 dark:bg-emerald-500/10', activeBar: 'bg-emerald-500' },
  mentor: { bg: 'from-amber-500 to-orange-600', text: 'text-amber-600 dark:text-amber-400', activeBg: 'bg-amber-50 dark:bg-amber-500/10', activeBar: 'bg-amber-500' },
  system_admin: { bg: 'from-rose-500 to-pink-600', text: 'text-rose-600 dark:text-rose-400', activeBg: 'bg-rose-50 dark:bg-rose-500/10', activeBar: 'bg-rose-500' },
}

function Tooltip({ children, content, collapsed }) {
  const [show, setShow] = useState(false)
  if (!collapsed) return children
  return (
    <div className="relative" onMouseEnter={() => setShow(true)} onMouseLeave={() => setShow(false)}>
      {children}
      <AnimatePresence>
        {show && (
          <motion.div
            initial={{ opacity: 0, x: -4 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -4 }}
            className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2.5 py-1.5 rounded-lg bg-slate-900 dark:bg-slate-700 text-white text-xs font-medium whitespace-nowrap shadow-elevated z-50 pointer-events-none"
          >
            {content}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function Sidebar() {
  const pathname = usePathname()
  const { user, logout } = useAuth()
  const { collapsed, mobileOpen, toggleCollapsed, closeMobile } = useSidebar()
  const [hoveredItem, setHoveredItem] = useState(null)

  const role = user?.role || 'student'
  const config = NAV_CONFIG[role] || NAV_CONFIG.student
  const colors = roleGradients[role] || roleGradients.student
  const RoleIcon = config.icon

  const handleLogout = () => {
    logout()
    closeMobile()
  }

  const isActiveRoute = (href) => {
    if (href === '/') return pathname === '/'
    return pathname.startsWith(href)
  }

  return (
    <aside
      className="flex flex-col h-full w-full bg-sidebar border-r border-sidebar-border"
      aria-label="Sidebar navigation"
    >
      {/* Logo */}
      <div className={cn(
        'flex items-center border-b border-sidebar-border transition-all duration-300',
        collapsed ? 'justify-center px-2 py-4' : 'gap-3 px-4 py-4'
      )}>
        <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-sm shadow-indigo-500/20">
          S
        </div>
        <AnimatePresence mode="wait">
          {!collapsed && (
            <motion.div
              key="brand"
              initial={{ opacity: 0, width: 0 }}
              animate={{ opacity: 1, width: 'auto' }}
              exit={{ opacity: 0, width: 0 }}
              className="min-w-0 overflow-hidden flex items-center gap-3"
            >
              <div className="min-w-0">
                <p className="font-bold text-sidebar-foreground text-sm leading-tight">Saarthi</p>
                <p className="text-[10px] text-muted-foreground truncate">Admission Platform</p>
              </div>
              <button
                onClick={toggleCollapsed}
                className="p-1 rounded-md hover:bg-sidebar-accent text-muted-foreground hover:text-foreground transition-all flex-shrink-0"
                aria-label="Collapse sidebar"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
        {collapsed && (
          <button
            onClick={toggleCollapsed}
            className="absolute -right-3 top-5 w-6 h-6 rounded-full border border-sidebar-border bg-sidebar flex items-center justify-center text-muted-foreground hover:text-foreground hover:border-foreground/20 transition-all shadow-soft z-10"
            aria-label="Expand sidebar"
          >
            <ChevronRight className="w-3 h-3" />
          </button>
        )}
      </div>

      {/* Role badge */}
      <AnimatePresence>
        {!collapsed && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="px-4 pt-4 pb-2 overflow-hidden"
          >
            <div className={cn('flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r', config.gradient, 'shadow-sm')}>
              <RoleIcon className="w-3.5 h-3.5 text-white" />
              <span className="text-xs font-semibold text-white">{config.label}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Navigation */}
      <nav className={cn('flex-1 overflow-y-auto scrollbar-hide', collapsed ? 'px-2 py-3' : 'px-3 py-3')}>
        <div className="space-y-0.5">
          {config.items.map((item, idx) => {
            const Icon = item.icon
            const isActive = isActiveRoute(item.href)

            return (
              <Tooltip key={item.key} content={item.label} collapsed={collapsed}>
                <Link
                  href={item.href}
                  onClick={closeMobile}
                  className={cn(
                    'flex items-center gap-3 rounded-lg transition-all duration-200 group relative',
                    collapsed ? 'justify-center p-2.5' : 'px-3 py-2.5',
                    isActive
                      ? `${colors.activeBg} ${colors.text} font-medium shadow-sm`
                      : 'text-muted-foreground hover:text-foreground hover:bg-sidebar-accent'
                  )}
                  onMouseEnter={() => setHoveredItem(item.href)}
                  onMouseLeave={() => setHoveredItem(null)}
                  aria-label={item.label}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <Icon className={cn('w-5 h-5 flex-shrink-0 transition-transform', isActive && 'scale-110', hoveredItem === item.href && !isActive && 'scale-110')} />
                  {!collapsed && <span className="text-sm truncate flex-1">{item.label}</span>}
                  {item.badge && !collapsed && (
                    <span className="px-1.5 py-0.5 text-[10px] font-bold rounded-full bg-red-500 text-white min-w-[18px] text-center leading-tight">
                      {item.badge}
                    </span>
                  )}
                  {item.badge && collapsed && (
                    <span className="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-red-500 text-white text-[8px] font-bold flex items-center justify-center">
                      {item.badge}
                    </span>
                  )}
                  {isActive && !collapsed && (
                    <div className={cn('absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-full', colors.activeBar)} />
                  )}
                </Link>
              </Tooltip>
            )
          })}
        </div>
      </nav>

      {/* User section */}
      <div className="border-t border-sidebar-border">
        <div className={cn('transition-all duration-300', collapsed ? 'p-2' : 'p-3')}>
          <Tooltip content="Profile" collapsed={collapsed}>
            <div className={cn(
              'flex items-center rounded-lg transition-all',
              collapsed ? 'justify-center p-1' : 'gap-3 px-3 py-2 bg-sidebar-accent/50 mb-2'
            )}>
              <div className={cn(
                'rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold flex-shrink-0 shadow-sm',
                collapsed ? 'w-8 h-8 text-xs' : 'w-8 h-8 text-xs'
              )}>
                {user?.full_name?.[0] || user?.email?.[0] || '?'}
              </div>
              {!collapsed && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-sidebar-foreground truncate leading-tight">{user?.full_name || 'User'}</p>
                  <p className="text-[10px] text-muted-foreground truncate">{user?.email || ''}</p>
                </div>
              )}
            </div>
          </Tooltip>
          <Tooltip content="Help & Support" collapsed={collapsed}>
            <Link
              href="/chat"
              onClick={closeMobile}
              className={cn(
                'flex items-center gap-3 rounded-lg text-muted-foreground hover:text-foreground hover:bg-sidebar-accent transition-all duration-200 mb-1',
                collapsed ? 'justify-center p-2.5' : 'px-3 py-2'
              )}
              aria-label="Help & Support"
            >
              <HelpCircle className="w-4 h-4 flex-shrink-0" />
              {!collapsed && <span className="text-sm">Help & Support</span>}
            </Link>
          </Tooltip>
          <Tooltip content="Sign Out" collapsed={collapsed}>
            <button
              onClick={handleLogout}
              className={cn(
                'flex items-center gap-3 rounded-lg text-muted-foreground hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 transition-all duration-200 w-full',
                collapsed ? 'justify-center p-2.5' : 'px-3 py-2'
              )}
              aria-label="Sign Out"
            >
              <LogOut className="w-4 h-4 flex-shrink-0" />
              {!collapsed && <span className="text-sm">Sign Out</span>}
            </button>
          </Tooltip>
        </div>
      </div>
    </aside>
  )
}
