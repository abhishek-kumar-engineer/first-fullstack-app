import { Component, inject } from '@angular/core';
import { LoaderService } from '../../../services/loader/loader';
@Component({
  selector: 'app-loader',
  standalone: true,
  imports: [],
  templateUrl: './loader.html',
  styleUrl: './loader.css',
})
export class Loader {
  readonly loader = inject(LoaderService);
}
