import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { Auth } from '../../../services/auth/auth';
import { Common } from '../../../services/common/common';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './reset-password.html',
  styleUrl: './reset-password.css',
})
export class ResetPassword {

  private authService = inject(Auth);
  private commonService = inject(Common);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  token: string = '';
  new_password: string = '';
  isLoading: boolean = false;
  successMsg: string = '';
  errorMsg: string = '';
  errors: string[] = [];

  constructor(
  ) { }

  ngOnInit(): void {
    // URL se token nikalo → /reset-password?token=xxx
    this.token = this.route.snapshot.queryParamMap.get('token') || '';

    if (!this.token) {
      this.errorMsg = 'Invalid reset link — please request a new one';
    }
  }

  onSubmit(): void {
    this.errorMsg = '';
    this.successMsg = '';
    this.errors = [];
    this.isLoading = true;

    this.commonService.postData('reset-password', {
      token: this.token,
      new_password: this.new_password
    }).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.successMsg = res.message;

        // 2 second baad login pe redirect
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err) => {
        this.isLoading = false;
        if (err.error?.errors) {
          this.errors = err.error.errors;     // multiple errors
        } else {
          this.errorMsg = err.error?.message || 'Something went wrong!';
        }
      }
    });
  }

}
