import raw from '../invitation.config.json';

export type InvitationConfig = {
	name: string;
	saveTheDate: string;
	date: string;
	venue: string;
	monogramInitial: string;
	monogramScript: string;
	monogramSubtitle: string;
	creditLogo: string;
	creditPrefix: string;
	creditUrl: string;
};

export const defaultConfig: InvitationConfig = raw;
