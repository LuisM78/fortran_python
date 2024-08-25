program fluid_simulation
    implicit none
    integer, parameter :: nx = 800, ny = 50, nt = 50000
    integer :: i, j, n
    real(8), parameter :: dt = 0.008, dx = 10.0 / (nx - 1), dy = 0.5 / (ny - 1)
    real(8), parameter :: rho = 1.0, nu = 0.1
    real(8) :: x_grid(nx), y_grid(ny)
    real(8) :: X(nx, ny), Y(nx, ny)
    real(8) :: u(ny, nx), v(ny, nx), p(ny, nx)
    character(len=100) :: filename
    character(len=100) :: dir_path
    character(len=100) :: full_path

    ! Specify the directory path
    dir_path = 'results/'

    ! Initialize grid
    do i = 1, nx
        x_grid(i) = (i - 1) * dx
    end do
    do j = 1, ny
        y_grid(j) = (j - 1) * dy
    end do
    do i = 1, nx
        do j = 1, ny
            X(i, j) = x_grid(i)
            Y(i, j) = y_grid(j)
        end do
    end do

    ! Initialize velocity and pressure fields
    u = 0.0
    v = 0.0
    p = 0.0

    ! Main simulation loop
    do n = 1, nt
        call update_velocity(u, v, p, rho, nu, dt, dx, dy, nx, ny)

        ! Print velocity and pressure fields for debugging
        if (mod(n, 50) == 0 .or. n == nt) then
            ! Print some of the values of u, v, and p to the console
            !print *, "Time step: ", n
            !print *, "Sample values of u (velocity in x direction) at various positions:"
            !do j = 1, min(ny, 10)  ! Print first 10 rows
            !    print *, (u(j, i), i = 1, min(nx, 10))  ! Print first 10 columns
            !end do

            !print *, "Sample values of v (velocity in y direction) at various positions:"
            !do j = 1, min(ny, 10)  ! Print first 10 rows
            !    print *, (v(j, i), i = 1, min(nx, 10))  ! Print first 10 columns
            !end do

            !print *, "Sample values of p (pressure) at various positions:"
            !do j = 1, min(ny, 10)  ! Print first 10 rows
            !    print *, (p(j, i), i = 1, min(nx, 10))  ! Print first 10 columns
            !end do

            ! Save data to file
            write(filename, '(I5.5, A)') n, '.txt'

            ! Concatenate the directory path and the filename
            full_path = trim(dir_path) // trim(filename)

            !  open(unit=20, file=filename, status='replace') from before
            ! Open the file in the specified directory
            open(unit=20, file=full_path, status='replace')
            
            ! Write the data with each row on a new line
            do j = 1, ny
                write(20, '(800F8.3)') (u(j, i), i = 1, nx)
            end do
            
            do j = 1, ny
                write(20, '(800F8.3)') (v(j, i), i = 1, nx)
            end do
            
            do j = 1, ny
                write(20, '(800F8.3)') (p(j, i), i = 1, nx)
            end do

            close(20)
        end if
    end do

contains

    subroutine update_velocity(u, v, p, rho, nu, dt, dx, dy, nx, ny)
        real(8), dimension(ny, nx), intent(inout) :: u, v
        real(8), dimension(ny, nx), intent(in) :: p
        real(8), intent(in) :: rho, nu, dt, dx, dy
        integer, intent(in) :: nx, ny
        real(8) :: diffusion
        integer :: i, j

        diffusion = 0.01 * nu

        ! Update u component of velocity
        do i = 2, nx - 1
            do j = 2, ny - 1
                u(j, i) = u(j, i) - u(j, i) * dt / dx * (u(j, i) - u(j, i - 1)) &
                             - v(j, i) * dt / dy * (u(j, i) - u(j - 1, i)) &
                             - dt / (2 * rho * dx) * (p(j, i + 1) - p(j, i - 1)) &
                             + diffusion * (dt / dx**2 * (u(j, i + 1) - 2 * u(j, i) + u(j, i - 1)) &
                             + dt / dy**2 * (u(j + 1, i) - 2 * u(j, i) + u(j - 1, i)))
            end do
        end do

        ! Update v component of velocity
        do i = 2, nx - 1
            do j = 2, ny - 1
                v(j, i) = v(j, i) - u(j, i) * dt / dx * (v(j, i) - v(j, i - 1)) &
                             - v(j, i) * dt / dy * (v(j, i) - v(j - 1, i)) &
                             - dt / (2 * rho * dy) * (p(j + 1, i) - p(j - 1, i)) &
                             + diffusion * (dt / dx**2 * (v(j, i + 1) - 2 * v(j, i) + v(j, i - 1)) &
                             + dt / dy**2 * (v(j + 1, i) - 2 * v(j, i) + v(j - 1, i)))
            end do
        end do

        ! Boundary conditions
        u(1, :) = 0.0
        u(ny, :) = 0.0
        v(1, :) = 0.0
        v(ny, :) = 0.0
        u(:, 1) = 0.5
        u(:, nx) = u(:, nx - 1)  ! Zero gradient condition at outlet
        v(:, 1) = 0.0
        v(:, nx) = v(:, nx - 1)  ! Zero gradient condition at outlet

    end subroutine update_velocity

end program fluid_simulation
