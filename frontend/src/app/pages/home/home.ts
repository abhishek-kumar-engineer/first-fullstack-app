import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  user: any = null;

  constructor(
    private authService: Auth,
    private router: Router
  ) { }

  ngOnInit(): void {
    // localStorage se user info lo
    this.user = this.authService.getUser();
  }

  logout(): void {
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
