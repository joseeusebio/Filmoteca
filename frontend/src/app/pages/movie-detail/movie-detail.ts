import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule, NgIf, DatePipe, DecimalPipe } from '@angular/common';
import { MatChipsModule, MatChip } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { RouterModule } from '@angular/router';

import { MovieService } from '../../services/movie.service';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  templateUrl: './movie-detail.html',
  styleUrls: ['./movie-detail.scss'],
  imports: [
    CommonModule,
    NgIf,
    DatePipe,
    DecimalPipe,
    RouterModule,
    MatChipsModule,
    MatChip,
    MatCardModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  providers: [MovieService],
})
export class MovieDetail {
  movie: any = null;
  isLoading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private movieService: MovieService
  ) {}

  ngOnInit(): void {
    const movieId = this.route.snapshot.paramMap.get('id');
    if (movieId) {
      this.movieService.getMovieById(movieId).subscribe((data) => {
        this.movie = data;
        this.isLoading = false;
      });
    }
  }

  goToHome(): void {
    this.router.navigate(['/']);
  }
}
