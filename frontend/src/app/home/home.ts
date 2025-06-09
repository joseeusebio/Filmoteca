import { Component } from '@angular/core';
import {
  NgIf,
  NgFor,
  DatePipe,
  DecimalPipe,
} from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule, MatChip } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule, MatButton } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';

import { MovieService } from '../services/movie.service';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.html',
  styleUrl: './home.scss',
  imports: [
    NgIf,
    NgFor,
    FormsModule,
    DatePipe,
    DecimalPipe,
    MatCardModule,
    MatChipsModule,
    MatChip,
    MatButtonModule,
    MatButton,
    MatIconModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
  ],
  providers: [MovieService],
})
export class Home {
  movies: any[] = [];
  isLoading = false;
  currentPage = 1;
  totalPages = 1;
  formOptions: any = {};
  filters: any = {};
  filteredCountries: string[] = [];
  filteredLanguages: string[] = [];
  countrySearch = '';
  languageSearch = '';

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadFormOptions();
    this.loadPage(1);
  }

  loadFormOptions(): void {
    this.movieService.getFormOptions().subscribe((options) => {
      this.formOptions = options;
      this.filteredCountries = [...options.production_countries];
      this.filteredLanguages = [...options.spoken_languages];
    });
  }

  loadPage(page: number = 1): void {
    this.isLoading = true;
    const params: any = { page };

    Object.entries(this.filters).forEach(([key, value]) => {
      if (Array.isArray(value) && value.length > 0) {
        params[key] = value;
      } else if (typeof value === 'string' && value.trim() !== '') {
        params[key] = value.trim();
      } else if (
        typeof value === 'number' || typeof value === 'boolean'
      ) {
        params[key] = value;
      }
    });

    this.movieService.getMoviesWithParams(params).subscribe((response) => {
      this.movies = response.data;
      this.currentPage = response.meta?.currentPage ?? 1;
      this.totalPages = response.meta?.totalPages ?? 1;
      this.isLoading = false;
    });
  }

  getPages(): number[] {
    const maxPagesToShow = 10;
    const half = Math.floor(maxPagesToShow / 2);
    if (this.totalPages === 0) return [];

    let start = Math.max(this.currentPage - half, 1);
    let end = start + maxPagesToShow - 1;

    if (end > this.totalPages) {
      end = this.totalPages;
      start = Math.max(end - maxPagesToShow + 1, 1);
    }

    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }

  goToPage(page: number): void {
    if (page !== this.currentPage && page >= 1 && page <= this.totalPages) {
      this.loadPage(page);
    }
  }

  goToFirst(): void {
    if (this.currentPage > 1) this.loadPage(1);
  }

  goToPrevious(): void {
    if (this.currentPage > 1) this.loadPage(this.currentPage - 1);
  }

  goToNext(): void {
    if (this.currentPage < this.totalPages) this.loadPage(this.currentPage + 1);
  }

  scrollToTop(): void {
    const content = document.querySelector('.content-scroll');
    content?.scrollTo({ top: 0, behavior: 'smooth' });
  }

  onFilterChange(): void {
    this.loadPage(1);
  }

  clearFilters(): void {
    this.filters = {};
    this.countrySearch = '';
    this.languageSearch = '';
    this.filteredCountries = [...this.formOptions.production_countries];
    this.filteredLanguages = [...this.formOptions.spoken_languages];
    this.loadPage(1);
  }

  filterCountries(): void {
    const search = this.countrySearch.toLowerCase();
    this.filteredCountries = this.formOptions.production_countries.filter((c: string) =>
      c.toLowerCase().includes(search)
    );
  }

  filterLanguages(): void {
    const search = this.languageSearch.toLowerCase();
    this.filteredLanguages = this.formOptions.spoken_languages.filter((l: string) =>
      l.toLowerCase().includes(search)
    );
  }

  resetToHome(): void {
    this.clearFilters();
    this.scrollToTop();
  }
}
