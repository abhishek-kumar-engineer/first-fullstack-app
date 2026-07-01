import { Component, EventEmitter, inject, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth } from '../../../services/auth/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  private authService = inject(Auth);
  private router = inject(Router);
  // emits when hamburger icon is clicked -> parent toggles sidebar collapsed state
  @Output() toggleSidebar = new EventEmitter<void>();

  workspaceMenuOpen = false;
  avatarMenuOpen = false;
  avatarInitials = '😊'; 

  // Replace with real values from your auth/user service
  currentUser = {
    email: 'testing@gmail.com',
    name: 'Test User',
    workspaceName: 'workspace',
    workspaceId: 'XXXXXXXXXXXX',
    openSharingId: 'XXXXXXXXXXXX'
  };

  copiedField: 'workspaceId' | 'openSharingId' | null = null;

  constructor() {
    this.currentUser = { ...this.currentUser, ...this.authService.getUser() };
    this.avatarInitials = this.currentUser.name ? this.currentUser.name.charAt(0).toUpperCase() : '😊';
    console.log('Navbar user:', this.currentUser);
  }

  onToggleSidebar(): void {
    this.toggleSidebar.emit();
  }

  toggleWorkspaceMenu(): void {
    this.workspaceMenuOpen = !this.workspaceMenuOpen;
    this.avatarMenuOpen = false; // only one dropdown open at a time
  }

  toggleAvatarMenu(): void {
    this.avatarMenuOpen = !this.avatarMenuOpen;
    this.workspaceMenuOpen = false;
  }

  closeAvatarMenu(): void {
    this.avatarMenuOpen = false;
  }

  copyToClipboard(value: string, field: 'workspaceId' | 'openSharingId'): void {
    navigator.clipboard?.writeText(value).then(() => {
      this.copiedField = field;
      setTimeout(() => {
        if (this.copiedField === field) {
          this.copiedField = null;
        }
      }, 1500);
    });
  }

  onSettings(): void {
    this.closeAvatarMenu();
    // hook route navigation here, e.g. this.router.navigateByUrl('/settings')
  }

  onPrivacyPolicy(): void {
    this.closeAvatarMenu();
  }

  onSendFeedback(): void {
    this.closeAvatarMenu();
  }

  onLogout(): void {
    this.closeAvatarMenu();
    // hook your auth service logout here
    this.authService.logout().subscribe({
      next: () => {
        this.authService.clearSession();       // localStorage clear
        this.router.navigate(['/login']);
      },
      error: () => {
        // API fail ho toh bhi local session clear karo
        this.authService.clearSession();
        this.router.navigate(['/login']);
      }
    });
  }
}
