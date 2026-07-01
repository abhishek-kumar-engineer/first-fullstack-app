import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Auth } from '../../../services/auth/auth';
import { Common } from '../../../services/common/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {

  private authService = inject(Auth);
  private commonService = inject(Common);
  private router = inject(Router);

  // Form fields
  formData = {
    name: '',
    email: '',
    password: ''
  };

  // UI state
  isLoading = false;
  errorMsg = '';
  successMsg = '';

  constructor(
  ) { }

  onSubmit(): void {
    this.errorMsg = '';
    this.successMsg = '';
    this.isLoading = true;

    this.commonService.postData('register', this.formData).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.successMsg = response.message;

        // 2 second baad login page pe redirect
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err.error?.message || 'Something went wrong!';
      }
    });
  }

}
