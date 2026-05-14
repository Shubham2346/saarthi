'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { users } from '@/lib/api'
import styles from './Sidebar.module.css'

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Dashboard', icon: '📊' },
  { href: '/chat', label: 'Ask Saarthi', icon: '💬' },
  { href: '/tasks', label: 'My Tasks', icon: '📋', roles: ['STUDENT'] },
  { href: '/documents', label: 'Documents', icon: '📄' },
  { href: '/tickets', label: 'Support Tickets', icon: '🎫' },
]

const ADMIN_ITEMS = [
  { href: '/admin/knowledge', label: 'Knowledge Base', icon: '📚', roles: ['ADMIN', 'SYSTEM_ADMIN'] },
  { href: '/admin/users', label: 'User Management', icon: '👥', roles: ['SYSTEM_ADMIN'] },
  { href: '/admin/templates', label: 'Task Templates', icon: '⚙️', roles: ['SYSTEM_ADMIN'] },
]

const MENTOR_ITEMS = [
  { href: '/mentor/students', label: 'My Students', icon: '👨‍🎓', roles: ['MENTOR'] },
]

export default function Sidebar() {
  const pathname = usePathname()
  const { user, logout, refreshUser } = useAuth()

  const handleRoleChange = async (e) => {
    const newRole = e.target.value;
    try {
      await users.update({ role: newRole.toLowerCase() });
      await refreshUser(); // Fetch updated user
      window.location.href = '/dashboard'; // Force reload to re-render all gated content
    } catch (err) {
      console.error("Failed to update role", err);
    }
  }

  const role = user?.role?.toUpperCase() || 'STUDENT'

  const filteredNavItems = NAV_ITEMS.filter(item => !item.roles || item.roles.includes(role))
  const filteredAdminItems = ADMIN_ITEMS.filter(item => !item.roles || item.roles.includes(role))
  const filteredMentorItems = MENTOR_ITEMS.filter(item => !item.roles || item.roles.includes(role))

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>
        <span className={styles.logoIcon}>🎓</span>
        <span className={styles.logoText}>Saarthi</span>
      </div>

      <nav className={styles.nav}>
        <div className={styles.section}>
          <span className={styles.sectionLabel}>Main</span>
          {filteredNavItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`${styles.navItem} ${pathname === item.href ? styles.active : ''}`}
            >
              <span className={styles.navIcon}>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </div>

        {filteredMentorItems.length > 0 && (
          <div className={styles.section}>
            <span className={styles.sectionLabel}>Mentor</span>
            {filteredMentorItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`${styles.navItem} ${pathname.startsWith(item.href) ? styles.active : ''}`}
              >
                <span className={styles.navIcon}>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        )}

        {filteredAdminItems.length > 0 && (
          <div className={styles.section}>
            <span className={styles.sectionLabel}>Admin</span>
            {filteredAdminItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`${styles.navItem} ${pathname.startsWith(item.href) ? styles.active : ''}`}
              >
                <span className={styles.navIcon}>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        )}
      </nav>

      <div className={styles.userSection}>
        <div className={styles.roleSwitcher}>
          <select 
            value={role} 
            onChange={handleRoleChange}
            className={styles.roleSelect}
            title="Demo Role Switcher"
          >
            <option value="STUDENT">Student</option>
            <option value="MENTOR">Mentor</option>
            <option value="ADMIN">Admin</option>
            <option value="SYSTEM_ADMIN">System Admin</option>
          </select>
        </div>
        <div className={styles.userInfo}>
          <div className={styles.avatar}>
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt="" referrerPolicy="no-referrer" />
            ) : (
              <span>{user?.full_name?.[0] || '?'}</span>
            )}
          </div>
          <div className={styles.userMeta}>
            <span className={styles.userName}>{user?.full_name || 'Student'}</span>
            <span className={styles.userRole}>{user?.role || 'student'}</span>
          </div>
        </div>
        <button onClick={logout} className={styles.logoutBtn} title="Sign out">
          ↗
        </button>
      </div>
    </aside>
  )
}
