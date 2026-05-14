export const ROLE_DASHBOARDS = {
  student: '/dashboard',
  admin: '/admin',
  mentor: '/mentor',
  department_coordinator: '/coordinator',
  system_admin: '/system-admin',
}

export function getDashboardByRole(role) {
  return ROLE_DASHBOARDS[role] || '/dashboard'
}

export const ROLE_LABELS = {
  student: 'Student',
  admin: 'Admin',
  mentor: 'Faculty Mentor',
  department_coordinator: 'Dept. Coordinator',
  system_admin: 'System Admin',
}

export const ROLE_COLORS = {
  student: { bg: 'bg-emerald-100 dark:bg-emerald-900/30', text: 'text-emerald-700 dark:text-emerald-400', dot: 'bg-emerald-500', badge: 'emerald' },
  admin: { bg: 'bg-indigo-100 dark:bg-indigo-900/30', text: 'text-indigo-700 dark:text-indigo-400', dot: 'bg-indigo-500', badge: 'indigo' },
  mentor: { bg: 'bg-blue-100 dark:bg-blue-900/30', text: 'text-blue-700 dark:text-blue-400', dot: 'bg-blue-500', badge: 'blue' },
  department_coordinator: { bg: 'bg-amber-100 dark:bg-amber-900/30', text: 'text-amber-700 dark:text-amber-400', dot: 'bg-amber-500', badge: 'amber' },
  system_admin: { bg: 'bg-purple-100 dark:bg-purple-900/30', text: 'text-purple-700 dark:text-purple-400', dot: 'bg-purple-500', badge: 'purple' },
}

export const ROLE_ROUTES = {
  student: ['/dashboard', '/admission', '/chat', '/tasks', '/documents', '/payment'],
  admin: ['/admin', '/admin/applications', '/admin/students', '/admin/documents', '/admin/knowledge', '/admin/analytics', '/admin/mentors', '/admin/tickets'],
  mentor: ['/mentor', '/mentor/students', '/mentor/notes', '/mentor/schedule'],
  department_coordinator: ['/coordinator', '/coordinator/students', '/coordinator/applications', '/coordinator/reports'],
  system_admin: ['/system-admin', '/system-admin/users', '/system-admin/roles', '/system-admin/settings', '/system-admin/audit', '/system-admin/monitoring'],
}

export function isRouteAuthorized(role, pathname) {
  const routes = ROLE_ROUTES[role]
  if (!routes) return false
  return routes.some(r => pathname === r || pathname.startsWith(r + '/'))
}
