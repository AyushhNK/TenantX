# TenantX Frontend

A modern Next.js frontend for the TenantX multi-tenant platform, providing a beautiful and responsive user interface for organization management, user authentication, and multi-tenant operations.

## 🚀 Features

- **Modern UI/UX** with Tailwind CSS and responsive design
- **JWT Authentication** with automatic token management
- **Multi-tenant Support** with organization switching
- **Role-based Access Control** (Admin, Manager, Employee)
- **Real-time Updates** for organization changes
- **User Management** with member invitations
- **Responsive Design** that works on all devices

## 🛠️ Technology Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Fetch API
- **Authentication**: JWT tokens with localStorage

## 📋 Prerequisites

- Node.js 18+ 
- npm or yarn
- TenantX Django backend running on `http://localhost:8000`

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd tenantfrontend
npm install
```

### 2. Configure Environment

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── auth/             # Authentication components
│   │   ├── LoginForm.tsx
│   │   └── SignupForm.tsx
│   └── dashboard/        # Dashboard components
│       ├── Dashboard.tsx
│       ├── OrganizationSwitcher.tsx
│       ├── InviteMemberForm.tsx
│       └── UserProfile.tsx
└── contexts/             # React contexts
    └── AuthContext.tsx   # Authentication context
```

## 🎯 Key Components

### Authentication Components

- **LoginForm**: User login with username/password
- **SignupForm**: User registration with organization creation
- **AuthContext**: Global authentication state management

### Dashboard Components

- **Dashboard**: Main dashboard with organization overview
- **OrganizationSwitcher**: Switch between user's organizations
- **InviteMemberForm**: Invite new members (admin only)
- **UserProfile**: Display user information

## 🔧 API Integration

The frontend integrates with the Django backend through the following endpoints:

### Authentication
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/signup/` - User registration

### Organization Management
- `GET /api/accounts/me/memberships/` - Get user memberships
- `POST /api/accounts/switch-org/` - Switch active organization
- `POST /api/accounts/organizations/{id}/invite/` - Invite member

## 🎨 UI/UX Features

### Design System
- **Color Scheme**: Blue primary with gray accents
- **Typography**: Inter font family
- **Components**: Consistent button styles, form inputs, and cards
- **Responsive**: Mobile-first design approach

### User Experience
- **Loading States**: Spinners and disabled states during API calls
- **Error Handling**: User-friendly error messages
- **Success Feedback**: Confirmation messages for actions
- **Smooth Transitions**: CSS transitions for better UX

## 🔒 Security Features

- **JWT Token Management**: Automatic token storage and refresh
- **Protected Routes**: Authentication-based access control
- **Input Validation**: Client-side form validation
- **Secure API Calls**: Authorization headers for authenticated requests

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

### Environment Variables

For production, set the following environment variables:

```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api
```

## 🧪 Testing

### Run Tests

```bash
npm test
```

### Run Linting

```bash
npm run lint
```

## 🔧 Development

### Code Style

- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Tailwind**: Utility-first CSS framework

### Adding New Features

1. Create components in the appropriate directory
2. Add TypeScript interfaces for data structures
3. Update the AuthContext if needed
4. Add proper error handling
5. Test on different screen sizes

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure Django backend has CORS configured
2. **Authentication Issues**: Check JWT token expiration
3. **API Connection**: Verify backend is running on correct port
4. **Build Errors**: Clear `.next` folder and reinstall dependencies

### Debug Mode

```bash
# Run with debug logging
DEBUG=* npm run dev
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation

---

**Happy Coding! 🎉**
