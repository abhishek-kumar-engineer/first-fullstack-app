import { Component, inject, OnInit } from '@angular/core';
import { Sidebar } from '../layout/sidebar/sidebar';
import { CommonModule } from '@angular/common';
import { Navbar } from '../layout/navbar/navbar';
import { Router, RouterOutlet } from '@angular/router';
import { Auth } from '../../services/auth/auth';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, Navbar, Sidebar, RouterOutlet],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  private authService = inject(Auth);
  private router = inject(Router);

  sidebarCollapsed = false;
  user: any = null;

  onToggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  ngOnInit(): void {
    // localStorage se user info lo
    // this.user = this.authService.getUser();
  }
}
