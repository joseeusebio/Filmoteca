import { Component } from '@angular/core';
import {
  NgIf,
  NgFor,
  DatePipe,
  DecimalPipe,
} from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule, MatChip } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule, MatButton } from '@angular/material/button';

import { MovieService } from '../services/movie.service';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.html',
  styleUrl: './home.scss',
  imports: [
    NgIf,
    NgFor,
    DatePipe,
    DecimalPipe,
    MatCardModule,
    MatChipsModule,
    MatChip,
    MatButtonModule,
    MatButton,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  providers: [MovieService],
})
export class Home {
  movies: any[] = [];
  nextUrl?: string;
  previousUrl?: string;
  isLoading = false;

  constructor(private movieService: MovieService) {}

  ngOnInit(): void {
    this.loadPage();
  }

  private extractCursor(url: string | undefined): string | undefined {
    if (!url) return undefined;
    try {
      const parsed = new URL(url);
      return parsed.searchParams.get('cursor') || undefined;
    } catch {
      return undefined;
    }
  }

  loadPage(url?: string): void {
    this.isLoading = true;
    const cursor = this.extractCursor(url);

    this.movieService.getMovies(cursor).subscribe((response) => {
      this.movies = response.data;
      this.nextUrl = response.meta?.next ?? undefined;
      this.previousUrl = response.meta?.previous ?? undefined;
      this.isLoading = false;
    });
  }

  scrollToTop(): void {
    const content = document.querySelector('.content-scroll');
    content?.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
