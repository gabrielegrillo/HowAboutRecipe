import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashRecipesComponent } from './dash-recipes.component';

describe('DashRecipesComponent', () => {
  let component: DashRecipesComponent;
  let fixture: ComponentFixture<DashRecipesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashRecipesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashRecipesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
