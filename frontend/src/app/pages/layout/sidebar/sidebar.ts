import { Component, inject, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

export interface SidebarItem {
  label: string;
  icon: string;   // bootstrap-icons class e.g. 'bi-house'
  route?: string;
  badge?: string;
}

export interface SidebarSection {
  title: string | null; // null = no header shown (top-level items like Home, Workspace..)
  items: SidebarItem[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class Sidebar {
  private router =  inject(Router);
  // controlled from parent (toggled by navbar's hamburger button)
  @Input() collapsed = false;

  activeLabel = 'Workspace';

  sections: SidebarSection[] = [
    {
      title: null,
      items: [
        { label: 'Home', icon: 'bi-house', route: '/dashboard/home' },
      ]
    },
    {
      title: 'Settings',
      items: [
        { label: 'Account', icon: 'bi-gear', route: '/dashboard/account' },
        { label: 'Security', icon: 'bi-shield-lock', route: '/dashboard/security' },
      ]
    },
    {
      title: 'AI/ML',
      items: [
        { label: 'Playground', icon: 'bi-magic' }
      ]
    }
  ];

  ngOnInit(): void {
    // this.activeLabel = this.sections[0].items[0].label;
    // current URL se active item set karo
    this.setActiveFromUrl(this.router.url);

    // route change hone pe active update karo
    this.router.events.subscribe(() => {
      this.setActiveFromUrl(this.router.url);
    });
  }

  setActive(item: SidebarItem): void {
    this.activeLabel = item.label;

    // Route hai toh navigate karo
    if (item.route) {
      this.router.navigate([item.route]);
    }
  }

  // ── URL se match karke active set karo ────────────
  private setActiveFromUrl(url: string): void {
    for (const section of this.sections) {
      for (const item of section.items) {
        if (item.route && url.includes(item.route)) {
          this.activeLabel = item.label;
          return;
        }
      }
    }
  }
}
