import NextAuth from 'next-auth';
import OsuProvider from 'next-auth/providers/osu';

export default NextAuth({
  providers: [
    OsuProvider({
      clientId: process.env.OSU_CLIENT_ID,
      clientSecret: process.env.OSU_CLIENT_SECRET,
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.id;
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
  },
});
