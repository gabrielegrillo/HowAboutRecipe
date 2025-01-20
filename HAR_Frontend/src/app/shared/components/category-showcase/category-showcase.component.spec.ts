import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoryShowcaseComponent } from './category-showcase.component';

describe('CategoryShowcaseComponent', () => {
  let component: CategoryShowcaseComponent;
  let fixture: ComponentFixture<CategoryShowcaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CategoryShowcaseComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CategoryShowcaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
