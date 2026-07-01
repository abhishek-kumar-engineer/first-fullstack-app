import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';


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
  // controlled from parent (toggled by navbar's hamburger button)
  @Input() collapsed = false;

  activeLabel = 'Workspace';

  sections: SidebarSection[] = [
    {
      title: null,
      items: [
        { label: 'Home', icon: 'bi-house' },
        { label: 'Learn', icon: 'bi-mortarboard' },
        { label: 'Workspace', icon: 'bi-grid-1x2' },
        { label: 'Recents', icon: 'bi-clock-history' },
        { label: 'Catalog', icon: 'bi-hdd-stack' },
        { label: 'Jobs & Pipelines', icon: 'bi-diagram-3' },
        { label: 'Compute', icon: 'bi-cpu' },
        { label: 'Discover', icon: 'bi-compass' },
        { label: 'Marketplace', icon: 'bi-shop' }
      ]
    },
    {
      title: 'SQL',
      items: [
        { label: 'SQL Editor', icon: 'bi-code-square' },
        { label: 'Queries', icon: 'bi-file-earmark-text' },
        { label: 'Dashboards', icon: 'bi-bar-chart' },
        { label: 'Genie Spaces', icon: 'bi-stars' },
        { label: 'Alerts', icon: 'bi-bell' },
        { label: 'Query History', icon: 'bi-clock-history' },
        { label: 'SQL Warehouses', icon: 'bi-database' }
      ]
    },
    {
      title: 'Data Engineering',
      items: [
        { label: 'Runs', icon: 'bi-list-check' },
        { label: 'Data Ingestion', icon: 'bi-cloud-arrow-up' },
        { label: 'Visual Data Prep', icon: 'bi-bounding-box' }
      ]
    },
    {
      title: 'AI/ML',
      items: [
        { label: 'Playground', icon: 'bi-magic' }
      ]
    }
  ];

  setActive(item: SidebarItem): void {
    this.activeLabel = item.label;
    // hook your router navigation here, e.g. this.router.navigateByUrl(item.route)
  }
}
