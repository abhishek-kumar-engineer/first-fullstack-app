import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {

  // Form fields
  formData = {
    name    : '',
    email   : '',
    password: ''
  };

  // UI state
  isLoading  = false;
  errorMsg   = '';
  successMsg = '';

  constructor(
    private authService: Auth,
    private router: Router
  ) {}

  onSubmit(): void {
    this.errorMsg   = '';
    this.successMsg = '';
    this.isLoading  = true;

    this.authService.postData('register', this.formData).subscribe({
      next: (response) => {
        this.isLoading  = false;
        this.successMsg = response.message;

        // 2 second baad login page pe redirect
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg  = err.error?.message || 'Something went wrong!';
      }
    });
  }

}
